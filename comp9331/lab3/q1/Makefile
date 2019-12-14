# Question: subsetList

CC=gcc
CFLAGS=-Wall -Werror

all: testSubsetList

testSubsetList : DLList.o  subsetList.o testSubsetList.o
	$(CC) -m32 -o testSubsetList DLList.o  subsetList.o testSubsetList.o

subsetList.o : subsetList.c   DLList.h 
	$(CC) -m32 -c subsetList.c

testSubsetList.o : testSubsetList.c   DLList.h 
	$(CC) -m32 -c testSubsetList.c

clean:
	rm -f testSubsetList subsetList.o testSubsetList.o core
