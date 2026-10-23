#include <algorithm>
#include <vector>
using namespace std;

int solution(int n, int m, vector<vector<int>> edge_list, int k, vector<int> gps_log) {
    (void)m; vector<vector<int>> graph(n + 1);
    for (const auto& edge : edge_list) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }
    const int INF = 1000000000; vector<int> dp(n + 1,INF); dp[gps_log[0]] = 0;
    for (int time = 1; time < k; ++time) {
        vector<int> next(n + 1,INF);
        for (int node = 1; node <= n; ++node) {
            int best = dp[node]; for (int neighbor : graph[node]) best = min(best,dp[neighbor]);
            if (best < INF) next[node] = best + (node != gps_log[time]);
        }
        dp = move(next);
    }
    return dp[gps_log.back()] < INF ? dp[gps_log.back()] : -1;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, int m, vector<vector<int>> edge_list, int k, vector<int> gps_log) {  // 시간·실제 지역별 GPS 수정 횟수 최소화
// (void)m; vector<vector<int>> graph(n + 1);  // 지역별 인접 도로 저장
// for (const auto& edge : edge_list) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }  // 양방향 간선 등록
// const int INF = 1000000000; vector<int> dp(n + 1,INF); dp[gps_log[0]] = 0;  // 첫 기록의 위치를 고정하고 최소 수정 수 저장
// for (int time = 1; time < k; ++time) {  // 다음 GPS 기록을 차례대로 보정하기
// vector<int> next(n + 1,INF);  // 현재 시각의 최소 수정 수 초기화
// for (int node = 1; node <= n; ++node) {  // 이번 시각의 실제 위치 고르기
// int best = dp[node]; for (int neighbor : graph[node]) best = min(best,dp[neighbor]);  // 제자리 또는 인접 지역에서 온 최솟값 구하기
// if (best < INF) next[node] = best + (node != gps_log[time]);  // 기록과 다르면 수정 한 번을 더하기
// }  // 블록 끝
// dp = move(next);  // 다음 기록의 기준 상태로 바꾸기
// }  // 블록 끝
// return dp[gps_log.back()] < INF ? dp[gps_log.back()] : -1;  // 마지막 기록의 위치로 도착할 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 시간과 실제 지역을 상태로 제자리 또는 인접 지역에서 이동할 때 기록과 다른 횟수 최소화
