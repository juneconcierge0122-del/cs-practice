

// g++ -std=c++11 leetcode198_house_robber.cpp -o leetcode198_house_robber

#include<iostream>
#include<vector>

using namespace std;

class Solution{
public:
    int rob(vector<int>& nums){
        int n = nums.size();
	vector<int> memo(n+2, 0);
	for (int i=n-1; i>=0; --i){
	    memo[i] = max(nums[i]+memo[i+2], memo[i+1]);
	}

	return memo[0];

    }
};

int main(){
    Solution solution;

    vector<int> nums = {1, 2, 3, 1};

    int result = solution.rob(nums);


    cout << "Input array: [";
    for (int i=0; i<nums.size(); i++){
        cout << nums[i];
        if (i < nums.size() - 1){
            cout << ", ";
        }
    }
    cout << "]\n";

    cout << "Output result: " << result << "\n";


    return 0;
}
