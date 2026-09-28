from typing import List
from functools import cache

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        return self.climbStairs(n-1)+self.climbStairs(n-2)

    def climbStairs_dp(self, n: int) -> int:
        if n <=2:
            return n

        dp = [0]*(n+1)
        dp[1], dp[2] = 1, 2
        for i in range(3, n+1):
            dp[i] = dp[i-1] + dp[i-2]

        return dp[n]

if __name__ == '__main__':
    solution = Solution()


    for test_case in [2, 3, 14, 45]:
        result = solution.climbStairs_dp(test_case)

        print(f"Input array: {test_case}")
        print(f"Output: {result}")

        print('----------------')
