#ifndef SEQLIST_OPS_H
#define SEQLIST_OPS_H

#include <stddef.h>
#include "seqlist.h"


/* Remove the minimum element from L (assuming it is unique)
 * The removed value is returned via min_value
 * The vacated position is filled by the last element
 */

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

#endif
