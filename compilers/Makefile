.PHONY: clean distclean default

CC=gcc
CFLAGS=-Wall

default: alan

lexer.c: lexer.l
	flex -s -o lexer.c lexer.l

lexer.o: lexer.c parser.h

parser.h parser.c: parser.y
	bison -dv -o parser.c parser.y

parser.o: parser.c

alan: lexer.o parser.o
	$(CC) $(CFLAGS) -o alan $^ -lfl

clean:
	$(RM) lexer.c parser.c parser.h parser.output *.o *~

distclean: clean
	$(RM) alan
