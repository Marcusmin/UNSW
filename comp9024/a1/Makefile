CC=dcc

puzzle: puzzle.c boardADT.o
	$(CC) puzzle.c boardADT.o -o puzzle -lm

boardADT.o: boardADT.c
	$(CC) -c boardADT.c

clean:
	rm *.o puzzle
