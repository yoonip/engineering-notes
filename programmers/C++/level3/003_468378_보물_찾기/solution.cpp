#include <algorithm>
#include <climits>
#include <vector>
using namespace std;
extern int excavate(int);

int solution(vector<int> depth, int money) {
    (void)money;
    int n = (int)depth.size();
    vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));
    vector<vector<int>> choice(n, vector<int>(n + 1, 0));
    for (int size = 1; size <= n; ++size) for (int left = 0; left + size <= n; ++left) {
        int right = left + size; long long best = LLONG_MAX;
        for (int middle = left; middle < right; ++middle) {
            long long cost = depth[middle] + max(dp[left][middle], dp[middle + 1][right]);
            if (cost < best) { best = cost; choice[left][right] = middle; }
        }
        dp[left][right] = best;
    }
    int left = 0, right = n;
    while (left < right) {
        int middle = choice[left][right], result = excavate(middle + 1);
        if (result == 0) return middle + 1;
        if (result < 0) right = middle;
        else left = middle + 1;
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// extern int excavate(int);  // 채점 환경이 제공하는 굴착 함수를 외부 선언
// int solution(vector<int> depth, int money) {  // 최악의 굴착 비용을 줄이는 위치를 골라 보물 찾기
// (void)money;  // 예산 내의 최악 비용을 보장하는 선택 순서 계산
// int n = (int)depth.size();  // 보물이 있을 수 있는 열 수 구하기
// vector<vector<long long>> dp(n + 1, vector<long long>(n + 1, 0));  // 반열린 열 구간의 최소 최악 굴착 비용 저장
// vector<vector<int>> choice(n, vector<int>(n + 1, 0));  // 각 구간에서 먼저 굴착할 열 저장
// for (int size = 1; size <= n; ++size) for (int left = 0; left + size <= n; ++left) {  // 작은 구간부터 길이순으로 계산
// int right = left + size; long long best = LLONG_MAX;  // 현재 구간의 오른쪽 경계와 최소 비용 후보 초기화
// for (int middle = left; middle < right; ++middle) {  // 첫 굴착 열의 모든 후보 검사
// long long cost = depth[middle] + max(dp[left][middle], dp[middle + 1][right]);  // 현재 굴착 비용과 양쪽 중 더 큰 후속 비용을 더하기
// if (cost < best) { best = cost; choice[left][right] = middle; }  // 최악 비용이 작은 열 선택
// }  // 블록 끝
// dp[left][right] = best;  // 최적 첫 선택의 최악 비용 저장
// }  // 블록 끝
// int left = 0, right = n;  // 아직 보물이 있을 수 있는 열 구간 초기화
// while (left < right) {  // 실제 굴착 응답에 따라 후보 구간 줄이기
// int middle = choice[left][right], result = excavate(middle + 1);  // 최적 열을 1부터 시작하는 번호로 굴착
// if (result == 0) return middle + 1;  // 보물을 찾으면 해당 열 반환
// if (result < 0) right = middle;  // 보물이 왼쪽이면 오른쪽 경계 줄이기
// else left = middle + 1;  // 보물이 오른쪽이면 왼쪽 경계 늘리기
// }  // 블록 끝
// return 0;  // 유효한 응답에서는 도달하지 않는 기본 반환
// }  // 블록 끝

// 풀이 요약
// 각 후보 구간에서 굴착 비용과 양쪽 최악 비용의 합을 최소화하는 열을 계산하고 실제 굴착 응답에 따라 구간 줄이기
