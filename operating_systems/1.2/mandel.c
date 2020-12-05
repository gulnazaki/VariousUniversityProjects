/*
 * mandel.c
 *
 * A program to draw the Mandelbrot Set on a 256-color xterm.
 *
 */

#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <signal.h>

#include "mandel-lib.h"

#define MANDEL_MAX_ITERATION 100000

#define perror_pthread(ret, msg) \
	do { errno = ret; perror(msg); } while (0)

/***************************
 * Compile-time parameters *
 ***************************/

sem_t *sem;

/*
 * Output at the terminal is is x_chars wide by y_chars long
*/
int y_chars = 50;
int x_chars = 90;

/*
 * The part of the complex plane to be drawn:
 * upper left corner is (xmin, ymax), lower right corner is (xmax, ymin)
*/
double xmin = -1.8, xmax = 1.0;
double ymin = -1.0, ymax = 1.0;
	
/*
 * Every character in the final output is
 * xstep x ystep units wide on the complex plane.
 */
double xstep;
double ystep;

void sigint(int a) {
	reset_xterm_color(1);
	kill(getpid(), SIGKILL);
}

struct thread_info_struct {
	pthread_t tid; /* POSIX thread id, as returned by the library */
	int thrid; /* Application-defined thread id */
	int thrcnt;
};

void *safe_malloc(size_t size)
{
	void *p;

	if ((p = malloc(size)) == NULL) {
		fprintf(stderr, "Out of memory, failed to allocate %zd bytes\n",
			size);
		exit(1);
	}

	return p;
}

int safe_atoi(char *s, int *val)
{
	long l;
	char *endp;

	l = strtol(s, &endp, 10);
	if (s != endp && *endp == '\0') {
		*val = l;
		return 0;
	} else
		return -1;
}

void usage(char *argv0)
{
	fprintf(stderr, "Usage: %s thread_count\n\n"
		"Exactly one argument required:\n"
		"    thread_count: The number of threads to create.\n",
		argv0);
	exit(1);
}

/*
 * This function computes a line of output
 * as an array of x_char color values.
 */
void compute_mandel_line(int line, int color_val[])
{
	/*
	 * x and y traverse the complex plane.
	 */
	double x, y;

	int n;
	int val;

	/* Find out the y value corresponding to this line */
	y = ymax - ystep * line;

	/* and iterate for all points on this line */
	for (x = xmin, n = 0; n < x_chars; x+= xstep, n++) {

		/* Compute the point's color value */
		val = mandel_iterations_at_point(x, y, MANDEL_MAX_ITERATION);
		if (val > 255)
			val = 255;

		/* And store it in the color_val[] array */
		val = xterm_color(val);
		color_val[n] = val;
	}
}

/*
 * This function outputs an array of x_char color values
 * to a 256-color xterm.
 */
void output_mandel_line(int fd, int color_val[])
{
	int i;
	
	char point ='@';
	char newline='\n';

	for (i = 0; i < x_chars; i++) {
		/* Set the current color, then output the point */
		set_xterm_color(fd, color_val[i]);
		if (write(fd, &point, 1) != 1) {
			perror("compute_and_output_mandel_line: write point");
			exit(1);
		}
	}

	/* Now that the line is done, output a newline character */
	if (write(fd, &newline, 1) != 1) {
		perror("compute_and_output_mandel_line: write newline");
		exit(1);
	}
}

void compute_and_output_mandel_line(int fd, int line, int thrcnt)
{
	/*
	 * A temporary array, used to hold color values for the line being drawn
	 */
	int ret, color_val[x_chars];

	compute_mandel_line(line, color_val);

	ret = sem_wait(&sem[(thrcnt+line-1)%thrcnt]);
	if (ret) {
		perror_pthread(ret, "semaphore_wait");
		exit(1);
	}
	output_mandel_line(fd, color_val);
	ret = sem_post(&sem[line%thrcnt]);
	if (ret) {
		perror_pthread(ret, "semaphore_post");
		exit(1);
	}
}

/* Start function for each thread */
void *thread_start_fn(void *arg)
{
	struct thread_info_struct *thr = arg;
	int line;
	for (line = thr->thrid; line < y_chars; line += thr->thrcnt) {
		compute_and_output_mandel_line(1, line, thr->thrcnt);
	}
	return NULL;
}

int main(int argc, char *argv[])
{
	signal(SIGINT,sigint);

	int i, ret, thrcnt;

	struct thread_info_struct *thr;

	if (argc != 2)
		usage(argv[0]);
	if (safe_atoi(argv[1], &thrcnt) < 0 || thrcnt <= 0) {
		fprintf(stderr, "`%s' is not valid for `thread_count'\n", argv[1]);
		exit(1);
	}

	xstep = (xmax - xmin) / x_chars;
	ystep = (ymax - ymin) / y_chars;

	/*
	 * draw the Mandelbrot Set with multiple threads
	 * Output is sent to file descriptor '1', i.e., standard output.
	 */

 	thr = safe_malloc(thrcnt * sizeof(*thr));
	sem = safe_malloc(thrcnt * sizeof(sem_t));

	for (i = 0; i < thrcnt; i++) {
		/* Initialize per-thread structure */
		thr[i].thrid = i;
		thr[i].thrcnt = thrcnt;

		if (i == thrcnt -1) sem_init(&sem[i], 0, 1);
		else sem_init(&sem[i], 0, 0);
		
		/* Spawn new thread */
		ret = pthread_create(&thr[i].tid, NULL, thread_start_fn, &thr[i]);
		if (ret) {
			perror_pthread(ret, "pthread_create");
			exit(1);
		}
	}

	/*
	 * Wait for all threads to terminate
	 */
	for (i = 0; i < thrcnt; i++) {
		ret = pthread_join(thr[i].tid, NULL);
		if (ret) {
			perror_pthread(ret, "pthread_join");
			exit(1);
		}
	}

	reset_xterm_color(1);
	return 0;
}
