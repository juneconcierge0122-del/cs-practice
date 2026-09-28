from typing import List
from functools import cache

class Solution:
    def rob(self, nums: List[int]) -> int:
        
        @cache
        def dp(i: int) -> int:
            if i>= len(nums): return 0

            return max(nums[i]+dp(i+2), dp(i+1))

        return dp(0)


if __name__ == '__main__':
    solution = Solution()

    test_nums1 = [1, 2, 3, 1]
    test_nums2 = [2, 7, 9, 3, 1]


    for test_case in [test_nums1, test_nums2]:
        result = solution.rob(test_case)

        print(f"Input array: {test_case}")
        print(f"Output: {result}")

        print('----------------')
