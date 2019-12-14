// testsubsetList.c 
// Written by Ashesh Mahidadia, Jan 2018 

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "DLList.h"

int subsetList(DLList L1, DLList L2); 

int main(int argc, char *argv[])
{
	char buffer[1024] ;
	char *line ;

	line=fgets(buffer, sizeof(buffer), stdin);
	DLList L1 = getDLListStr(line);
	line=fgets(buffer, sizeof(buffer), stdin);
	DLList L2 = getDLListStr(line);

	fprintf(stdout, "L1: ");
	putDLList(stdout, L1);
	fprintf(stdout, "L2: ");
	putDLList(stdout, L2);

	int ans = subsetList(L1, L2);

	fprintf(stdout, "returns: %d\n", ans);

	freeDLList(L1);
	freeDLList(L2);

	return 0;

}
