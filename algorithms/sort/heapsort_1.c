/*
 * Heap sort [max heap]
 *
 * gcc -std=c99 -Wall -o heapsort heapsort_1.c
 *
 *
 * */


#include <stdio.h>

#define MAX_N 100

static void swap(int *a, int *b){
    int t=*a;
    *a = *b;
    *b = t;
}

// max_heap establish
// 逐一把 heap[i] 往上浮到正確位置（sift-up）

static void build_max_heap(int heap[], int n){
    for (int i=1; i<n; i++){
        int c = i;
        while( c != 0 ){
            int root = (c-1)/2;
            if (heap[root] >= heap[c])
                break;
            swap(&heap[root], &heap[c]);
            c= root;
        }
    }
}

// sift-down
// 讓 heap[root] 往下沉，作用範圍限制在 [0, n)

static void sift_down(int heap[], int root, int n){
    while(1){
        int c = 2*root+1;   // 左子節點

        if (c >= n)
            break;          // 沒有子節點

        if (c+1 < n && heap[c] <heap[c+1])
            c++;            // 選較大的子節點

        if (heap[root] >= heap[c])
            break;          // 已滿足 max heap 性質

        swap(&heap[root], &heap[c]);
        root = c;

    }
}

// 由小到大排序 in-place, O(nlogn)
//

void heap_sort(int heap[], int n){
    build_max_heap(heap, n);

    for (int j=n-1; j>0; j--){
        swap(&heap[0], &heap[j]);  // 最大值放到 unsorted 尾端
        sift_down(heap, 0, j);     // 修復剩下的 heap
    }
}


/** ----- 測試用工具 -----  **/
 
static void print_array(const char *label, const int a[], int n){

    printf("%s", label);
    if (n == 0)
        printf(" (empty)");

    for (int i=0; i<n; i++)
        printf(" %d", a[i]);

    printf("\n");
}




static int is_sorted(const int a[], int n){
    for (int i=1; i<n; i++)
        if (a[i-1] > a[i])
            return 0;
    return 1;
}



// 0: pass; 1: fail
static int run_test(const char *name, const int input[], int n){
    int heap[MAX_N];

    if (n > MAX_N){
        printf( "--- %s: n=%d 超過 MAX_N=%d,  跳過 \n\n", name, n, MAX_N);
    }

    for (int i=0; i<n; i++)
        heap[i] = input[i];

    printf("--- %s (n = %d)\n", name, n);
    print_array("  input:", heap, n);
    heap_sort(heap, n);
    print_array("  sorted:", heap, n);

    if (is_sorted(heap, n)){
        printf("  PASS\n\n");
        return 0;
    }
    printf("  FAIL\n\n");
    return 1;

}



int main(void)
{
    int failed = 0;
 
    int t_basic[]     = {4, 1, 3, 9, 7};
    int t_asc[]       = {1, 2, 3, 4, 5, 6};
    int t_desc[]      = {9, 8, 7, 6, 5, 4};
    int t_same[]      = {5, 5, 5, 5};
    int t_dup[]       = {3, 1, 3, 2, 1, 2};
    int t_neg[]       = {-3, 7, 0, -8, 2, -1};
    int t_one[]       = {42};
    int t_two[]       = {2, 1};
    int t_pow2[]      = {8, 3, 6, 1, 7, 2, 5, 4};   /* 完滿二元樹 */
    int t_odd[]       = {10, 20, 15, 30, 40, 50, 45, 5, 25};
 
    failed += run_test("basic",            t_basic, 5);
    failed += run_test("already sorted",   t_asc,   6);
    failed += run_test("reverse sorted",   t_desc,  6);
    failed += run_test("all identical",    t_same,  4);
    failed += run_test("with duplicates",  t_dup,   6);
    failed += run_test("negative numbers", t_neg,   6);
    failed += run_test("single element",   t_one,   1);
    failed += run_test("two elements",     t_two,   2);
    failed += run_test("full binary tree", t_pow2,  8);
    failed += run_test("odd size",         t_odd,   9);
    failed += run_test("empty",            t_one,   0);   /* n=0，不讀任何元素 */
 
    printf("=== %s\n", failed == 0 ? "all tests passed" : "some tests FAILED");
 
    /* ---------- 互動輸入版本（需要時取消註解） ----------
 *  int heap[MAX_N], no;
 *      
 *  printf("\n Enter no of elements: ");
 *  if (scanf("%d", &no) != 1) {
 *      printf("輸入不是整數\n");
 *      return 1;
 *  }
 *  if (no < 0 || no > MAX_N) {
 *      printf("元素個數需介於 0 到 %d\n", MAX_N);
 *      return 1;
 *  }
 *  printf(" Enter the nos: ");
 *  for (int i = 0; i < no; i++) {
 *      if (scanf("%d", &heap[i]) != 1) {
 *          printf("第 %d 個輸入不是整數\n", i + 1);
 *          return 1;
 *      }
 *  }
 *  heap_sort(heap, no);
 *  print_array(" The sorted array is:", heap, no);
 *  ---------------------------------------------------- */
 
    return failed == 0 ? 0 : 1;
}
