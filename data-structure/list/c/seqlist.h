#ifndef SEQLIST_H
#define SEQLIST_H

#include <stddef.h>

/* -- type definition --*/

typedef int ElemType;


typedef enum{
    LIST_OK = 0,
    LIST_ERROR = 1,
    LIST_INDEX_ERROR = 2,
    LIST_ALLOC_ERROR = 3,
} Status;


typedef struct{
    ElemType *elem;
    int length;
    int capacity;
} SqList;

#define LIST_INIT_CAPACITY 10
#define LIST_INCREMENT 10

/* -- Basic operation -- */

Status InitList(SqList *L);

void DestroyList(SqList *L);

int Empty(const SqList *L);

int Length(const SqList *L);

Status GetElem(const SqList *L, int i, ElemType *e);

int LocateElem(const SqList *L, ElemType e);

Status ListInsert(SqList *L, int i, ElemType e);

Status ListDelete(SqList *L, int i, ElemType *e);

void PrintList(const SqList *L);

#endif
