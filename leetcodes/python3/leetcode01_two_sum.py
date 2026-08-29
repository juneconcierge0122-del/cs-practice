from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, num in enumerate(nums):
            if target-num in seen:
                return [seen[target-num], i]
            seen[num] = i


if __name__ == '__main__':
    solution = Solution()

    test_nums = [2, 7, 11, 15]
    test_target = 9

    result = solution.twoSum(test_nums, test_target)

    print(f"Input array: {test_nums}")
    print(f"Input target: {test_target}")

    print(f"Output indices: {result}")
