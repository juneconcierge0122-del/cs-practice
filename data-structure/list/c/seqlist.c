#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "seqlist.h"

Status InitList(SqList *L){
    //L->elem=NULL;
    L->elem=malloc(LIST_INIT_CAPACITY * sizeof(ElemType));

    if (L->elem==NULL){
        L->length=0;
	L->capacity=0;
	return LIST_ALLOC_ERROR;
    }

    L->length=0;
    L->capacity=LIST_INIT_CAPACITY;
    return LIST_OK;
}

void DestroyList(SqList *L){
    free(L->elem);
    L->elem=NULL;
    L->length=0;
    L->capacity=0;
}

int Length(const SqList *L){
    return L->length;
}

int Empty(const SqList *L){
    //return 1 if L->length==0 else 0 --> python 
    return (L->length==0)? 1:0;
}


int LocateElem(const SqList *L, ElemType e){
    // insert e before i-th position
    //
    for (int i=0; i<L->length; i++){
        if (L->elem[i] == e) return i+1;
    }
    return LIST_OK;

}

Status GetElem(const SqList *L, int i , ElemType *e){
    if (i < 1 || i> L->length) return LIST_INDEX_ERROR;
    *e = L->elem[i-1];
    return LIST_OK;
}


Status ListDelete(SqList *L, int i, ElemType *e){
    // valid i in [1, length]
    if (i < 1 || i> L->length) return LIST_INDEX_ERROR;
    *e = L->elem[i-1];
    for(int j = i; j<L->length; j++){
        L->elem[j-1] = L->elem[j];
    }

    L->length --;
    return LIST_OK;
    
}


Status ListInsert(SqList *L, int i, ElemType e){
    if (i < 1 || i > L->length+1 ){
        return LIST_INDEX_ERROR;
    }

    if( L->length == L->capacity){
	return LIST_ALLOC_ERROR;
    }

    for(int j = L->length; j>=i; j--){
        L->elem[j] = L->elem[j-1];
    }

    L->elem[i-1] = e;
    L->length++;

    return LIST_OK;
}

void PrintList(const SqList *L){
    for (int i=0; i< L->length; i++){
        printf("%d ", L->elem[i]);
    }
    printf("\n");
}


/*
 * NOTE: L is declared as `SqList *L` (a pointer), not `SqList L`.
 * A pointer holds the ADDRESS of a struct, not the struct itself.
 * To access a member through a pointer, you must dereference it first:
 *     (*L).length      <-- explicit dereference, then access member
 *     L->length         <-- shorthand for the line above, same thing
 *
 * Rule of thumb: if the parameter type has a `*`, use `->`.
 *                if it's a plain struct (no `*`), use `.`.
 */
