
## [65] cannot pass


class Solution:
    def minOperations(self, nums: list[int]) -> int:
        n = len(nums)
        ops = [0]*n

        for i in range(len(nums)):
            if nums[i] <10:
                ops[i] = 0

            elif nums[i]<100:
                if nums[i]%2==0:
                    if 10 <=nums[i]<=15:
                        ops[i] = (nums[i]-8)/2
                    elif 16 <=nums[i]<=23:
                        ops[i] = abs(nums[i]-22)/2
                    else:
                        ten_digit = (nums[i])/10
                        ops[i] = min(abs(nums[i] - ten_digit*11), abs(nums[i] - (ten_digit+1)*11)) / 2
                else:
                    ten_digit = (nums[i])/10
                    ops[i] = min(abs(nums[i] - ten_digit*11), abs(nums[i] - (ten_digit-1)*11)) / 2

            else:
                str_nums = str(nums[i])
                left = len(str_nums)-1
                right = 0
                #print(str_nums[left])
                diff = []

                while left>right:
                    if str_nums[left] == str_nums[right]:
                        diff.append(0)
                    else:
                        diff_elem = abs(int(str_nums[left]) - int(str_nums[right]))
                        diff.append(diff_elem)
                    left-=1
                    right+=1

                ops_elem = 0
                for di in range(len(diff)):
                    ops_elem += diff[di]*10**(di)/2
                ops[i] = ops_elem
                # print(ops)
        ans = int(sum(ops))
        return ans


## test by claude

import random, time
def is_pal(v): s=str(v); return s==s[::-1]

def brute(x):
    k=0
    while True:
        if x-2*k > 0 and is_pal(x-2*k): return k
        if is_pal(x+2*k): return k

def user(x):
    if x < 10:return 0
    if x < 100:
        if x %2 ==0:
            if 10 <= x <= 15: return (x-8)/2
            elif 16 <= x <=23: return abs(x-22)/2
            else:
                t = x/10; return min(abs(x-t*11), abs(x-(t+1)*11))/2
        else:
            t=x/10; return min(abs(x-t*11), abs(x-(t-1)*11))/2
    s = str(x); l, r = len(s)-1; diff=[]
    while l>r:
        diff.append(abs(int(s[l])) - int(s[r])); l-=1; r+=1
    return sum(d*10**i/2 for i, d in enumerate(diff))

def min_ops(x: int) -> int:
    s = str(x); L=len(s); t = x&1
    h = (L+1) //2
    p = int(s[:h])
    cands = []

    # 1. same length, same prefic --> mirror(p-1), mirror(p), mirror(p+1)

    for q in (p-1, p, p+1):
        qs = str(q)
        if len(qs) == h and q>0:
            cands.append(int(qs+qs[:L//2][::-1]))

    # 2. L-1, L, L+1; first-d has the same parity with x; 
    #    d0..0d & d9..9d

    for length in (L-1, L, L+1):
        if length < 1: continue

        for d in range(1+(1-t), 10, 2):
            ds = str(d)
            if length == 1:
                cands.append(d)
            else:
                mid = length - 2
                cands.append(int(ds+'0'*mid+ds))
                cands.append(int(ds+'9'*mid+ds))
    return min( abs(x-c) for c in cands if c>0 and (c&1) ==1 )//2


class Solution:
    def minOperations(self, nums):
        return sum(map(min_ops, nums))

print("[65] test", user(65), "Correct", min_ops(65), "Brute-force", brute(65))
