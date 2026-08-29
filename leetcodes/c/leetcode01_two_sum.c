
//  gcc -std=c99 -Wall -o leetcode01_two_sum leetcode01_two_sum.c

#include <stdio.h>
#include <stdlib.h>

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    for (int i=0; i<numsSize; i++){
        for (int j=i+1; j<numsSize; j++){
            if (nums[i]+nums[j] == target){
                int* result = (int*)malloc(2*sizeof(int));
                if (result == NULL) return NULL;

                result[0]=i;
                result[1]=j;
                *returnSize = 2;
                return result;
            }
        }
    }
    *returnSize = 0;
    return NULL;
}

int main(){

    int nums[] = {2, 7, 11, 15};
    int numsSize = sizeof(nums) / sizeof(nums[0]); // length of array
    int target = 9;


    int returnSize = 0;
    int* result = twoSum(nums, numsSize, target, &returnSize);

    if (result != NULL && returnSize == 2){
        printf("輸入的陣列:[");
        for (int i =0; i<numsSize; i++){
            printf("%d", nums[i]);
            if (i<numsSize-1){
                printf(", ");
            }
        }
        printf("]\n");
        // ----------------

        printf("Target Sum: %d\n", target);
        printf("Found indices: [%d, %d]\n", result[0], result[1]);


        free(result);
    } else{
        printf("Not find!\n");
    }


    return 0;
}
