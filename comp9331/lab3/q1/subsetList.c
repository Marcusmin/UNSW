// subsetList.c 
// Written by Ashesh Mahidadia, Jan 2018

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "DLList.h"
#include <stdbool.h>


/* 
    You will submit only this one file.

    Implement the function "subsetList" below. Read the exam paper for 
    detailed specification and description of your task.  

    - DO NOT modify code in the file DLList.h . 
    - You can add helper functions in this file.  
    - DO NOT add "main" function in this file. 
    
*/


int subsetList(DLList L1, DLList L2){
	if (DLListIsEmpty(L2)){
		return 1;
	}
	if (DLListIsEmpty(L1) || DLListLength(L1) < DLListLength(L2)){
		return 0;
	}
	int l1[DLListLength(L1)], l2[DLListLength(L2)], l1_index = 0, l2_index = 0;


	while (L1->first != NULL){
		l1[l1_index++] = L1->first->value;
		L1->first = L1->first->next;
	}

	while (L2->first != NULL){
		l2[l2_index++] = L2->first->value;
		L2->first = L2->first->next;
	}
	int i, j;
	for (i = 0; i < l2_index; i++){
		for (j = 0; j < l1_index; j++){
			if (l1[j] == l2[i]){
				break; 
			}			
		}
		if (j == l1_index){
			return 0;
		}
	}
	return 1;
	

}



