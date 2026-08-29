
/* 
 * C program to sort an array based on heap sort algorithm (MAX heap)
 *   ref: https://github.com/argonautica/sorting-algorithms/blob/master/C/heapsort.c
 */

#include <stdio.h>

void main(){
    int heap[10], no, i, j, c, root, temp;

    printf("\n Enter no of elements:");
    scanf("%d", &no);
    printf("\n Enter the nos:");
    for (i=0; i<no; i++){
        scanf("%d", &heap[i]);
    }
    for (i=1; i<no; i++){
        c=i;
        do {
            root = (c-1)/2;
            if (heap[root] < heap[c]) {
                temp = heap[root];
                heap[root] = heap[c];
                heap[c] = temp;
            }
            c = root;
        } while(c!=0);
    }

    printf("Heap array: ");
    for(i=0; i<no; i++){
        printf("%d\t", heap[i]);
    }

    for(j = no-1; j>0; j--){
        temp = heap[0];
        heap[0] = heap[j];
        heap[j] = temp;
        root = 0;

        while(1){
            c = 2*root+1;
            if (c>=j) break;                        // 沒有子節點
            if (c+1<j && heap[c] < heap[c+1]) c++;  // 選較大的子節點
            if (heap[root] >= heap[c]) break;  // 已滿足 heap 性質

            temp = heap[root];
            heap[root] = heap[c];
            heap[c] = temp;
            root = c;
        }
    }
    printf("\n The sorted array is: ");
    for (i=0; i<no; i++)
        printf("\t %d", heap[i]);

    printf("\n Complexity: \n Best case = Avg case = Worst case = O(n log n) \n");
}
