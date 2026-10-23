#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<vector<int>> triangle) {
    vector<int> dp = triangle.back();
    for (int row = (int)triangle.size() - 2; row >= 0; --row) for (int c = 0; c < (int)triangle[row].size(); ++c) dp[c] = triangle[row][c] + max(dp[c], dp[c + 1]);
    return dp[0];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> triangle) {  // 아래쪽 두 경로 중 큰 합을 골라 위로 누적
// vector<int> dp = triangle.back();  // 마지막 행에서 시작하는 최대 합 초기화
// for (int row = (int)triangle.size() - 2; row >= 0; --row) for (int c = 0; c < (int)triangle[row].size(); ++c) dp[c] = triangle[row][c] + max(dp[c], dp[c + 1]);  // 아래의 두 경로 중 큰 합에 현재 값을 더하기
// return dp[0];  // 꼭대기에서 시작하는 최대 경로 합 반환
// }  // 블록 끝

// 풀이 요약
// 삼각형의 아래 행부터 두 자식 경로 합의 최댓값에 현재 값을 더하며 꼭대기까지 올라가기
