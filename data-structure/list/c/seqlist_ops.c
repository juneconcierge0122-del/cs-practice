
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "seqlist.h"
#include "seqlist_ops.h"



Status DeleteMin(SqList *L, ElemType *min_value){
    if (L->length ==0){
        fprintf(stderr, "Error: list is empty, cannot delete min.\n");
        return LIST_ERROR;

    }

    int min_index = 0;

    ElemType min_val = L->elem[0];

    for (int i=1; i<L->length; i++){
        if (L->elem[i] < min_val){
            min_val = L->elem[i];
            min_index = i;
        }

    }

    ElemType last_val = L->elem[L->length-1];

    L->elem[min_index] = last_val;
    L->length--;

    *min_value = min_val;
    return LIST_OK;
}

Status Reverse(SqList *L){
    int i = 0;
    int j = L->length-1;


    while (i<j){
        ElemType tmp = L->elem[i];
        L->elem[i] = L->elem[j];
	L->elem[j] = tmp;

	i++;
	j--;
    }

    return LIST_OK;

}
