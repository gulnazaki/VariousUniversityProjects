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
#define SHELL_EXECUTABLE_NAME "shell" /* executable for shell */

struct proc {
	pid_t pid;
	int id;
	char *name;
    char priority; //"h" for high or "l" for low
	struct proc *next;
};

/*HEAD is always SHELL*/
struct proc *active_proc;
struct proc *head;

int nproc;

/*
check_priority() looks for high_priority procs and
 returns 1 if HIGH exists, else 0
*/
static int check_priority() {
	struct proc *current = head;
	while (current != NULL) {
		if (current->priority == 'h') {
			return 1;
		}
		current = current->next;
	}
	return 0;
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

static void ins_proc(pid_t new_pid, int id, char *process) {
	struct proc *new_proc;
	new_proc = (struct proc*)malloc(sizeof(struct proc));
	new_proc->pid = new_pid;
	new_proc->id = id;
	new_proc->name = process;
	new_proc->priority = 'l';
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
	printf("%s inserted in list, id =%d, PID=%ld\n",process, id, (long)new_pid);
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


static void update_list(int id)
{
    struct proc *current;
    struct proc *prev;
    current = head;
    if (current->id == id) {
		head = current->next;
	}
	else {
		while (current->id != id) {
			prev = current;
			current = current->next;
		}
		prev->next = current->next;
	}
    //current points to the process who we must put again in the right place
    if (current->priority == 'h') {
        //after sched_set_high, put the process at the head of the list
        current->next = head;
        head = current;
    }
    else {
        //after sched_set_low
        struct proc *last;
        last = head;
        while(last->next != NULL) {
            //ends at the last process in list
            last = last->next;
        }
        last->next = current;
        current->next = NULL;
    }
}

/* Send SIGKILL to a task determined by the value of its
 * scheduler-specific id.
 */
static int sched_kill_task_by_id(int del_id) {
	//if process list is empty finish execution of parent
	struct proc *current = head;
	struct proc *prev;
	if (current == NULL) return 1;

	if (current->id == del_id) {
		head = current->next;
	}

	else {
		while (current != NULL && current->id != del_id) {
			prev = current;
			current = current->next;
		}
		if (current == NULL) return 1;

		prev->next = current->next;
	}

	printf("%s deleted from list, id =%d, PID=%ld\n",current->name, del_id, (long)current->pid);
	kill(current->pid,SIGKILL);
	free(current);
	return 0;
}

/* Print a list of all tasks currently being scheduled.  */
static void
sched_print_tasks(void)
{
	struct proc *current = head;
	if(current == NULL) return;
	do {

		if (current == active_proc) printf("active-> ");
		printf("%d) Name = %s, Pid = %ld, Priority =%c \n\n",current->id,current->name,(long)current->pid,current->priority);
	} while((current = current->next) != NULL);
}

/* Create a new task.  */
static void
sched_create_task(char *executable)
{
	char *exec = strdup(executable);
	pid_t pid = fork();
		if (pid < 0) {
			perror("main: fork");
			exit(1);
		}
		if (pid == 0) {
			fork_procs(executable);
			exit(1);
		}
		ins_proc
		(pid,nproc++,exec);
}

/* Set high priority to a task. *//*NEW*/
static void sched_set_high(int id)
{
    struct proc *current;
    current = head;
    while(current != NULL) {
        if (current->id == id) break;   //process exists
        current = current->next;
    }
    if (current == NULL) { //whole list was searched with no result
        printf("No process with ID=%d was found\n",id);
        return;
    }
    if (current->priority == 'h') {
        printf("Process has already HIGH priority\n");
        return;
    }
    current->priority = 'h';    //changge priority
    update_list(id);
    printf("Process with ID = %d was set with HIGH priority!\n",id);
}

/* Set LOW priority to a task. *//*LOW*/
static void sched_set_low(int id)
{
    struct proc *current;
    current = head;
    while(current != NULL) {
        if (current->id == id) break;   //process exists
        current = current->next;
    }
    if (current == NULL) { //whole list was searched with no result
        printf("No process with ID=%d was found\n",id);
        return;
    }
    if (current->priority == 'l') {
        printf("Process has already LOW priority\n");
        return;
    }
    current->priority = 'l';    //change priority
    update_list(id);
    printf("Process with ID = %d was set with LOW priority!\n",id);

}

/* Process requests by the shell.  */
static int
process_request(struct request_struct *rq)
{
	switch (rq->request_no) {
		case REQ_PRINT_TASKS:
			sched_print_tasks();
			return 0;

		case REQ_KILL_TASK:
			return sched_kill_task_by_id(rq->task_arg);

		case REQ_EXEC_TASK:
			sched_create_task(rq->exec_task_arg);
			return 0;

		case REQ_HIGH_TASK:
	        sched_set_high(rq->task_arg);
	        return 0;

	    case REQ_LOW_TASK:
	        sched_set_low(rq->task_arg);
	        return 0;


		default:
			return -ENOSYS;
	}
}

/*
 * SIGALRM handler
 */
static void
sigalrm_handler(int signum)
{
	kill(active_proc->pid,SIGSTOP);
}

/*
 * SIGCHLD handler
 */
static void
sigchld_handler(int signum)
{
	int status;

	for (;;) {
		pid_t p = waitpid(-1, &status, WUNTRACED | WNOHANG);
		if (p < 0) {
			perror("waitpid");
			exit(1);
		}
		if (p == 0) break;
		//printf("CHILD\n");
		explain_wait_status(p,status);
		//if (active_proc->pid != p) break;
		if (WIFEXITED(status) || WIFSIGNALED(status)) {
			/* a child has died */
			if (active_proc->pid != p) {
				del_proc(p);
				break;
			}
			if (WIFEXITED(status)) del_proc(p);
			active_proc = active_proc->next;
			if (!active_proc) active_proc = head;
			if (head == NULL) {
				printf("\nEverything functioned properly\n");
				exit(0);
			}
		}
		else if (WIFSTOPPED(status)) {
			/* a child has stopped due to SIGSTOP/SIGTSTP, etc */
			if (active_proc->pid != p) break;
			active_proc = active_proc->next;
			if (!active_proc) active_proc = head;
		}
		/*
		next check if the next must not be continued
		(if it is low priority when high priority processes exist )
		*/
		if (check_priority()) {
			if (active_proc->priority == 'l') {
				active_proc = head;
				//return to head of list-bypass all LOW process
				// one HIGH process at least exists at the start of the list
			}
		}
		alarm(SCHED_TQ_SEC);
		//printf("Process continues: %d\n",active_proc->pid );
		kill(active_proc->pid,SIGCONT);
	}
}

/* Disable delivery of SIGALRM and SIGCHLD. */
static void
signals_disable(void)
{
	sigset_t sigset;

	sigemptyset(&sigset);
	sigaddset(&sigset, SIGALRM);
	sigaddset(&sigset, SIGCHLD);
	if (sigprocmask(SIG_BLOCK, &sigset, NULL) < 0) {
		perror("signals_disable: sigprocmask");
		exit(1);
	}
}

/* Enable delivery of SIGALRM and SIGCHLD.  */
static void
signals_enable(void)
{
	sigset_t sigset;

	sigemptyset(&sigset);
	sigaddset(&sigset, SIGALRM);
	sigaddset(&sigset, SIGCHLD);
	if (sigprocmask(SIG_UNBLOCK, &sigset, NULL) < 0) {
		perror("signals_enable: sigprocmask");
		exit(1);
	}
}


/* Install two signal handlers.
 * One for SIGCHLD, one for SIGALRM.
 * Make sure both signals are masked when one of them is running.
 */
static void
install_signal_handlers(void)
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

static void
do_shell(char *executable, int wfd, int rfd)
{
	char arg1[10], arg2[10];
	char *newargv[] = { executable, NULL, NULL, NULL };
	char *newenviron[] = { NULL };

	sprintf(arg1, "%05d", wfd);
	sprintf(arg2, "%05d", rfd);
	newargv[1] = arg1;
	newargv[2] = arg2;
	printf("PID = %ld, starting...\n", (long)getpid());
	printf("I am %s, PID = %ld\n",executable, (long)getpid());
	raise(SIGSTOP);
	execve(executable, newargv, newenviron);

	/* execve() only returns on error */
	perror("scheduler: child: execve");
	exit(1);
}

/* Create a new shell task.
 *
 * The shell gets special treatment:
 * two pipes are created for communication and passed
 * as command-line arguments to the executable.
 */
static void
sched_create_shell(char *executable, int *request_fd, int *return_fd)
{
	pid_t p;
	int pfds_rq[2], pfds_ret[2];

	if (pipe(pfds_rq) < 0 || pipe(pfds_ret) < 0) {
		perror("pipe");
		exit(1);
	}

	p = fork();
	if (p < 0) {
		perror("scheduler: fork");
		exit(1);
	}

	if (p == 0) {
		/* Child */
		close(pfds_rq[0]);
		close(pfds_ret[1]);
		do_shell(executable, pfds_rq[1], pfds_ret[0]);
		assert(0);
	}
	/* Parent */
	close(pfds_rq[1]);
	close(pfds_ret[0]);
	*request_fd = pfds_rq[0];
	*return_fd = pfds_ret[1];
	ins_proc(p,0,"shell");
}

static void
shell_request_loop(int request_fd, int return_fd)
{
	int ret;
	struct request_struct rq;

	/*
	 * Keep receiving requests from the shell.
	 */
	for (;;) {
		if (read(request_fd, &rq, sizeof(rq)) != sizeof(rq)) {
			perror("scheduler: read from shell");
			fprintf(stderr, "Scheduler: giving up on shell request processing.\n");
			break;
		}

		signals_disable();
		ret = process_request(&rq);
		signals_enable();

		if (write(return_fd, &ret, sizeof(ret)) != sizeof(ret)) {
			perror("scheduler: write to shell");
			fprintf(stderr, "Scheduler: giving up on shell request processing.\n");
			break;
		}
	}
}

int main(int argc, char *argv[])
{
	// we are thinking of shell as a process too (the first)
	nproc = argc;
	active_proc = NULL;
	head = NULL;

	/* Two file descriptors for communication with the shell */
	static int request_fd, return_fd;

	/* Create the shell. */
	sched_create_shell(SHELL_EXECUTABLE_NAME, &request_fd, &return_fd);


	pid_t pid;

	int i;
	for (i = 1; i<nproc ; i++) {
		//initializing processes
		pid = fork();
		if (pid < 0) {
			perror("main: fork");
			exit(1);
		}
		if (pid == 0) {
			fork_procs(argv[i]);
			exit(1);
		}
		ins_proc(pid,i,argv[i]);
	}

	/* Wait for all children to raise SIGSTOP before exec()ing. */
	wait_for_ready_children(nproc);

	/* Install SIGALRM and SIGCHLD handlers. */
	install_signal_handlers();
	active_proc = head;
	alarm(SCHED_TQ_SEC);
	kill(active_proc->pid, SIGCONT);

	if (nproc == 0) {
		fprintf(stderr, "Scheduler: No tasks. Exiting...\n");
		exit(1);
	}

	shell_request_loop(request_fd, return_fd);

	/* Now that the shell is gone, just loop forever
	 * until we exit from inside a signal handler.
	 */
	while (pause())
		;

	/* Unreachable */
	fprintf(stderr, "Internal error: Reached unreachable point\n");
	return 1;
}
