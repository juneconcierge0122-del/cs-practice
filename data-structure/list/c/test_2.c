//
// gcc -Wall -Wextra -std=c99 seqlist.c seqlist_ops.c test_2.c -o test2
// ./test2
//
//



#include <stdio.h>
#include <stdlib.h>
#include "seqlist.h"
#include "seqlist_ops.h"

int main(void){
    SqList L;
    ElemType e;
    Status s;

    InitList(&L);
    // DeleteMin
    
    s = DeleteMin(&L, &e);
    printf("Test1 (empty list): status=%d (expect LIST_ERROR=%d)\n", s, LIST_ERROR);

    // ---- 測試 2: 最小值在最前面 ----
    // 10 20 30 -> 刪除 10 -> 用最後一個(30)補到 index 0 -> 剩 30 20
    ListInsert(&L, 1, 10);
    ListInsert(&L, 2, 20);
    ListInsert(&L, 3, 30);
    s = DeleteMin(&L, &e);
    printf("Test2 (min at front): status=%d, deleted=%d (expect 10)\n", s, e);
    printf("  after: ");
    PrintList(&L);   // 期望輸出: 30 20

    // ---- 測試 3: 最小值在最後面 ----
    DestroyList(&L);
    InitList(&L);
    ListInsert(&L, 1, 30);
    ListInsert(&L, 2, 20);
    ListInsert(&L, 3, 10);   // 最小值剛好是最後一個
    s = DeleteMin(&L, &e);
    printf("Test3 (min at back): status=%d, deleted=%d (expect 10)\n", s, e);
    printf("  after: ");
    PrintList(&L);   // 期望輸出: 30 20  (這是特別要注意的邊界:min_index 剛好等於 length-1)

    // ---- 測試 4: 最小值在中間 ----
    DestroyList(&L);
    InitList(&L);
    ListInsert(&L, 1, 30);
    ListInsert(&L, 2, 10);
    ListInsert(&L, 3, 20);
    s = DeleteMin(&L, &e);
    printf("Test4 (min in middle): status=%d, deleted=%d (expect 10)\n", s, e);
    printf("  after: ");
    PrintList(&L);   // 期望輸出: 30 20

    // ---- 測試 5: 只剩一個元素時刪除 ----
    DestroyList(&L);
    InitList(&L);
    ListInsert(&L, 1, 42);
    s = DeleteMin(&L, &e);
    printf("Test5 (single element): status=%d, deleted=%d (expect 42)\n", s, e);
    printf("  length after: %d (expect 0)\n", Length(&L));

    // ---- 測試 6: 連續刪到空,確認不會 over-delete ----
    DestroyList(&L);
    InitList(&L);
    ListInsert(&L, 1, 5);
    ListInsert(&L, 2, 3);
    ListInsert(&L, 3, 8);
    ListInsert(&L, 4, 1);
    while (Length(&L) > 0) {
        DeleteMin(&L, &e);
        printf("  deleted %d, remaining length=%d\n", e, Length(&L));
    }
    s = DeleteMin(&L, &e);   // 表已空,這次應該安全地回傳錯誤
    printf("Test6 (delete after empty): status=%d (expect LIST_ERROR=%d)\n", s, LIST_ERROR);

    DestroyList(&L);


    printf("-------------------\n");

    SqList L1, L2, L3, L4;

    InitList(&L1);
    InitList(&L2);
    InitList(&L3);
    InitList(&L4);

    ListInsert(&L1, 1, 1);
    ListInsert(&L1, 2, 2);
    ListInsert(&L1, 3, 3);
    ListInsert(&L1, 4, 4);


    ListInsert(&L2, 1, 11);
    ListInsert(&L2, 2, 27);
    ListInsert(&L2, 3, 33);
    ListInsert(&L2, 4, 42);
    ListInsert(&L2, 5, 59);
    
    ListInsert(&L3, 5, 999);
    printf("Insert at i=5 on empty list: status=%d (expect LIST_INDEX_ERROR=%d)\n", s, LIST_INDEX_ERROR);
    ListInsert(&L3, 1, 999);


    Reverse(&L1);
    Reverse(&L2);
    Reverse(&L3);
    Reverse(&L4);

    PrintList(&L1); 
    PrintList(&L2); 
    PrintList(&L3); 
    PrintList(&L4); 



    return 0;
}
