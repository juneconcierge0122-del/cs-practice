//  gcc -Wall -Wextra -std=c99 seqlist.c test.c -o test

#include <stdio.h>
#include "seqlist.h"

int main(void){
    SqList L;
    ElemType e;
    Status s;

    s = InitList(&L);
    printf("InitList: status=%d, length=%d, capacity=%d\n", s, Length(&L), L.capacity);
    printf("Empty after init: %d (expect 1)\n", Empty(&L));


    ListInsert(&L, 1, 10);
    ListInsert(&L, 2, 20);
    ListInsert(&L, 3, 30);
    printf("After inserting 10, 20, 30:");
    PrintList(&L);

    // insert in the middle; and insert in the beginning
    ListInsert(&L, 1, 99);
    printf("After inserting 99 at position 1:");
    PrintList(&L);


    // Test invalid i
    s = ListInsert(&L, 0, 100);
    printf("Insert at i=0: status=%d (expect LIST_INDEX_ERROR=%d)\n", s, LIST_INDEX_ERROR);
    s = ListInsert(&L, 100, 100);
    printf("Insert at i=100: status=%d (expect LIST_INDEX_ERROR=%d)\n", s, LIST_INDEX_ERROR);

    // Test `GetElem`
    s = GetElem(&L, 2, &e);
    printf("GetElem(2): status=%d, value=%d (expect 10)\n", s, e);


    // Test `LocateElem`
    //
    printf("LocateElem(20): %d (expect 3)\n", LocateElem(&L, 20));
    printf("LocateElem(999): %d (expect 0, not found) \n", LocateElem(&L, 999));

    // Test `ListDelete`
    s = ListDelete(&L, 1, &e);
    printf("ListDelete(1): status=%d, deleted value=%d (expect 99)", s, e);
    printf("After delete: ");
    PrintList(&L);

    // Test re-allocate
    for (int i=0; i<15; i++){
        ListInsert(&L, Length(&L)+1, i);
    }
    printf("After bulk insert: length=%d, capacity=%d\n", Length(&L), L.capacity);
    PrintList(&L);


    // Test DestroyList
    DestroyList(&L);
    printf("After destroy: elem is %s (expect NULL)\n", L.elem==NULL? "NULL":"Not NULL");
    return 0;
}
