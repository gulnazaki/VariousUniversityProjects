all: zing zing2

zing: zing.o main.o
	gcc -o zing zing.o main.o
		
zing2: zing2.o main.o
	gcc -o zing2 zing2.o main.o

main.o:	main.c
	gcc -Wall -c main.c

zing2.o: zing2.c
	gcc -Wall -c zing2.c
