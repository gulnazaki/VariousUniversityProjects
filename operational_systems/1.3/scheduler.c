#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <assert.h>

#include <sys/wait.h>
#include <sys/types.h>

#include "proc-common.h"
#include "request.h"

/* Compile-time parameters. */
#define SCHED_TQ_SEC 2                /* time quantum */
#define TASK_NAME_SZ 60               /* maximum size for a task's name */

struct proc {
	pid_t pid;
	char *name;
	struct proc *next;
};

struct proc *active_proc;
struct proc *head;

static void ins_proc(pid_t new_pid, char *process) {
	struct proc *new_proc;
	new_proc = (struct proc*)malloc(sizeof(struct proc));
	new_proc->pid = new_pid;
	new_proc->name = process;
	new_proc->next = NULL;
	if (head == NULL) {
		head = new_proc;
	} else {
		struct proc *current = head;
		while(current->next != NULL) {
			current = current->next;
		}
		current->next = new_proc;
	}
	printf("%s inserted in list, PID=%ld\n",process, (long)new_pid);
}

static void del_proc(pid_t del_pid) {
	//if process list is empty finish execution of parent
	struct proc *current = head;
	struct proc *prev;
	if (current == NULL) return;
	
	if (current->pid == del_pid) {
		head = current->next;
	}

	else {
		while (current != NULL && current->pid != del_pid) {
			prev = current;
			current = current->next;
		}
		if (current == NULL) return;

		prev->next = current->next;
	}

	printf("%s deleted from list, PID=%ld\n",current->name, (long)del_pid);
	free(current);
}

/*
 * SIGALRM handler
 */
static void sigalrm_handler(int signum)
{
	//printf("ALARM\n");
	//printf("process stopped: %d\n", active_proc->pid);
	kill(active_proc->pid,SIGSTOP);
}

/*
 * SIGCHLD handler
 */
static void sigchld_handler(int signum)
{
	//printf("SIGCHILD CAUGHT\n");
	int status;

	for (;;) {
		pid_t p = waitpid(-1, &status, WUNTRACED | WNOHANG);
		if (p < 0) {
			perror("waitpid");
			exit(1);
		}
		if (p == 0) break;
		explain_wait_status(p,status);
		if (WIFEXITED(status) || WIFSIGNALED(status)) {
			/* a child has died */
			if (active_proc->pid != p) {
				del_proc(p);
				break;
			}
			active_proc = active_proc->next;
			if (!active_proc) active_proc = head;
			del_proc(p);
			if (head == NULL) {
				printf("\nEverything functioned properly\n");
				exit(0);
			}
		}
		else if (WIFSTOPPED(status)) {
			/* a child has stopped due to SIGSTOP/SIGTSTP, etc */
			active_proc = active_proc->next;
			if (!active_proc) active_proc = head;
		}
		alarm(SCHED_TQ_SEC);
		//printf("Process continues: %d\n",active_proc->pid );
		kill(active_proc->pid,SIGCONT);
	}
}

/* Install two signal handlers.
 * One for SIGCHLD, one for SIGALRM.
 * Make sure both signals are masked when one of them is running.
 */
static void install_signal_handlers(void)
{
	sigset_t sigset;
	struct sigaction sa;

	sa.sa_handler = sigchld_handler;
	sa.sa_flags = SA_RESTART;
	sigemptyset(&sigset);
	sigaddset(&sigset, SIGCHLD);
	sigaddset(&sigset, SIGALRM);
	sa.sa_mask = sigset;
	if (sigaction(SIGCHLD, &sa, NULL) < 0) {
		perror("sigaction: sigchld");
		exit(1);
	}

	sa.sa_handler = sigalrm_handler;
	if (sigaction(SIGALRM, &sa, NULL) < 0) {
		perror("sigaction: sigalrm");
		exit(1);
	}

	/*
	 * Ignore SIGPIPE, so that write()s to pipes
	 * with no reader do not result in us being killed,
	 * and write() returns EPIPE instead.
	 */
	if (signal(SIGPIPE, SIG_IGN) < 0) {
		perror("signal: sigpipe");
		exit(1);
	}
}

static void fork_procs(char *process) {
	char *newargv[]={process,NULL};
	char *newenviron[]= { NULL };
    printf("PID = %ld, starting...\n", (long)getpid());
	printf("I am %s, PID = %ld\n",process, (long)getpid());
	raise(SIGSTOP);
	execve(process,newargv,newenviron);
	perror("execve");
    exit(127);
}


int main(int argc, char *argv[])
{
	int nproc = argc-1; /* number of proccesses goes here */
	active_proc = NULL;
	head = NULL;

	pid_t pid;
	/*
	 * For each of argv[1] to argv[argc - 1],
	 * create a new child process, add it to the process list.
	 */

	int i;
	for (i = 0; i<nproc ; i++) {
		//initializing processes
		pid = fork();
		if (pid < 0) {
			perror("main: fork");
			exit(1);
		}
		if (pid == 0) {
			fork_procs(argv[i+1]);
			exit(1);
		}
		ins_proc(pid,argv[i+1]);
	}
	/* Wait for all children to raise SIGSTOP before exec()ing. */
	wait_for_ready_children(nproc);

	/* Install SIGALRM and SIGCHLD handlers. */
	install_signal_handlers();
	active_proc = head;
	alarm(SCHED_TQ_SEC);
	kill(active_proc->pid, SIGCONT);	/* send signal for first process to start */

	if (nproc == 0) {
		fprintf(stderr, "Scheduler: No tasks. Exiting...\n");
		exit(1);
	}
	/* loop forever  until we exit from inside a signal handler. */
	while (pause());

	/* Unreachable */
	fprintf(stderr, "Internal error: Reached unreachable point\n");
	return 1;
}
