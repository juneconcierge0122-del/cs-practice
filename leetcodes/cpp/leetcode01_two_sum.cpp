

// g++ -std=c++11 leetcode01_two_sum.cpp -o leetcode01_two_sum

#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

class Solution{
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;

        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];

            // Method 2: count()
            if (seen.count(complement)) {
                   // 1 -> true
                   return {seen[complement], i};
            }

            seen[nums[i]] = i;
        }
        return {};
    }
};

int main(){
    Solution solution;

    vector<int> nums = {2, 7, 11, 15};
    int target = 9;

    vector<int> result = solution.twoSum(nums, target);


    cout << "Input array: [";
    for (int i=0; i<nums.size(); i++){
        cout << nums[i];
        if (i < nums.size() - 1){
            cout << ", ";
        }
    }
    cout << "]\n";

    cout << "Target Sum: " << target << "\n";
    if (!result.empty()) {
        cout << "Found indices: [" << result[0] << ", " << result[1] << "]\n";
    } else {
        cout << "Not found\n";
    }


    return 0;
}
