#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "boardADT.h"
#define MAX 10000

int main(void){
	int len_a, len_b, num_a, num_b;
	char *a = (char*)malloc(MAX * sizeof(char));
	char *b = (char*)malloc(MAX * sizeof(char));
	fgets(a, MAX, stdin);
	fgets(b, MAX, stdin);
	len_a = strlen(a);
	len_b = strlen(b); 
	printf("start: a = %s", a);
	printf("goal: b = %s", b);
	if (len_a != len_b){
        printf("start and goal must have same numbers, please try again\n");
        return EXIT_FAILURE;
    }
	Np c = (Np)malloc(len_a * sizeof(N));
	Np d = (Np)malloc(len_b * sizeof(N));
	num_a = assign(a, c);
	num_b = assign(b, d);
    free(a);
    free(b);

	int p_a = get_partity(num_a);
    int p_b = get_partity(num_b);
	if (p_a == -1 || p_b == -1){
	   printf("you must enter n^2 numbers, please try again.\n");
	   return EXIT_FAILURE;
	}

    int valid_a = valid(c, num_a);
    int valid_b = valid(d, num_b);
    if (valid_a == 0 || valid_b == 0){
    	printf("you miss some numbers, please try again.\n");
    	return EXIT_FAILURE;	
    }	

	int sum_a = get_sum(c, p_a, num_a);
	int sum_b = get_sum(d, p_b, num_b);

	if (sum_a % 2 == sum_b % 2){
        printf("solvable\n");
	}
	else{
    	printf("unslovable\n");
	}
    free(c);
    free(d);
	return EXIT_SUCCESS;
}
