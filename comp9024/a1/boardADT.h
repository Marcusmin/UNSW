#ifndef _BOARDADT_H_
#define _BOARDADT_H_
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAX 10000
typedef struct Node{
    int data;
}N, *Np;
int assign(char *a, Np c);
int get_partity(int a);
int valid(Np a, int n);
int get_sum(Np a, int p, int n);
#endif
