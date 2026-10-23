#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

int solution(vector<vector<int>> matrix_sizes) {
    int n = (int)matrix_sizes.size(); vector<int> dimensions{matrix_sizes[0][0]};
    for (const auto& size : matrix_sizes) dimensions.push_back(size[1]);
    vector<vector<long long>> dp(n, vector<long long>(n,0));
    for (int length = 2; length <= n; ++length) for (int start = 0; start + length <= n; ++start) {
        int end = start + length - 1; dp[start][end] = LLONG_MAX;
        for (int middle = start; middle < end; ++middle) dp[start][end] = min(dp[start][end], dp[start][middle] + dp[middle + 1][end] + 1LL * dimensions[start] * dimensions[middle + 1] * dimensions[end + 1]);
    }
    return (int)dp[0][n - 1];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> matrix_sizes) {  // 행렬 구간의 마지막 곱셈 위치를 나눠 비용 비교
// int n = (int)matrix_sizes.size(); vector<int> dimensions{matrix_sizes[0][0]};  // 행렬 곱의 차원 경계 배열 만들기
// for (const auto& size : matrix_sizes) dimensions.push_back(size[1]);  // 각 행렬의 열 수를 차례대로 붙이기
// vector<vector<long long>> dp(n, vector<long long>(n,0));  // 연속 행렬 구간별 최소 곱셈 수 저장
// for (int length = 2; length <= n; ++length) for (int start = 0; start + length <= n; ++start) {  // 짧은 행렬 구간부터 처리
// int end = start + length - 1; dp[start][end] = LLONG_MAX;  // 현재 구간의 최소 비용 초기화
// for (int middle = start; middle < end; ++middle) dp[start][end] = min(dp[start][end], dp[start][middle] + dp[middle + 1][end] + 1LL * dimensions[start] * dimensions[middle + 1] * dimensions[end + 1]);  // 마지막 곱셈의 분할점마다 양쪽 비용과 결합 비용 비교
// }  // 블록 끝
// return (int)dp[0][n - 1];  // 전체 행렬 곱의 최소 연산 수 반환
// }  // 블록 끝

// 풀이 요약
// 연속 행렬 구간의 마지막 곱셈 분할점마다 양쪽 최적 비용과 결합 비용 비교
