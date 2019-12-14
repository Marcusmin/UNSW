#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "boardADT.h"
#define MAX 10000

int assign(char *a, Np c){
    int i = 0;
    char p = ' ';
    char *part = NULL;
    part = strtok(a, &p);
    while (part != NULL){
        if (*part == 'b'){
            (c+i)->data = 0;
            i++;
        }
        else {
            (c+i)->data = atoi(part);
            i++;
        }
        part = strtok(NULL, &p);
    }
    return i;
}

int get_partity(int a){
    int temp = sqrt(a);
    if (pow(temp, 2) != a){
        return -1;
    }
    if (a%2 == 0){
        return 0;
    }
    else{
        return 1;
    }
}

int valid(Np a, int n){
	int i, j, result = 0, sum = (n-1)*n/2;
	for(i = 0; i < n; i++){
		result += (a+i)->data;
		for(j = i+1; j < n; j++){
			if((a+i)->data == (a+j)->data){
				return 0;
			}
		}
	}
	if(result != sum){
		return 0;
	}
	return 1;
}

int get_sum(Np a, int p, int n){
    int count = 0, i, j, zero, row = 1;
    if (p == 0){
        for(i = 0; i < n; i++){
            if ((a+i)->data == 0){
                zero = i+1;
                while(zero > sqrt(n)){
                    zero -= sqrt(n);
                    row++;
                }
            }
            else{
                for(j = i+1; j < n; j++){
                    if((a+j)->data != 0 && (a+i)->data > (a+j)->data){
                        count++;
                    }
                    else{
                        continue;
                    }
                }
            }
        }
        return (count + row);
    }
    else{
        for(i = 0; i < n; i++){
            if ((a+i)->data == 0){
                continue;
            }
            else{
                for(j = i+1; j < n; j++){
                    if((a+j)->data != 0 && (a+i)->data > (a+j)->data){
                        count++;
                    }
                    else{
                        continue;
                    }
                }
            }
        }
        return count;
    }
}



