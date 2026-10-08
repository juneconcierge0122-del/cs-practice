

// g++ -std=c++11 leetcode121_buy_and_sell.cpp -o leetcode121_buy_and_sell

#include <iostream>
#include <vector>
using namespace std;

class Solution{
public:
    int maxProfit(vector<int>& prices){
        int ans=9, mi=prices[0];
        for(int& v:prices){
            ans=max(ans, v-mi);
            mi=max(mi,v);
        }
        return ans;
    }
};

int main(){
    Solution solution;

    vector<int> prices1 = {7,1,5,3,6,4};
    int target1 = 5;

    int result1 = solution.maxProfit(prices1);


    cout << "Input array: [";
    for (int i=0; i<prices1.size(); i++){
        cout << prices1[i];
        if (i < prices1.size() - 1){
            cout << ", ";
        }
    }
    cout << "]\n";

    cout << "Target Profit: " << target1 << "\n";
    cout << "Test Output: " << result1 << "\n";

    return 0;
}
