#include <vector>
#include <algorithm>
using namespace std;

int solution(int n, int m, vector<vector<int>> edge_list, int k, vector<int> gps_log) {
    vector<vector<int>> graph(n + 1);
    for (auto edge : edge_list) {
        graph[edge[0]].push_back(edge[1]);
        graph[edge[1]].push_back(edge[0]);
    }
    const int INF = 1000000000;
    vector<int> dp(n + 1, INF);
    dp[gps_log[0]] = 0;
    for (int time = 1; time < k; ++time) {
        vector<int> next_dp(n + 1, INF);
        for (int node = 1; node <= n; ++node) {
            int best = dp[node];
            for (int neighbor : graph[node]) best = min(best, dp[neighbor]);
            next_dp[node] = best + (node != gps_log[time]);
        }
        dp.swap(next_dp);
    }
    int answer = dp[gps_log.back()];
    return answer < INF ? answer : -1;
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 가져오기. vector는 가변 길이 배열.
// #include <algorithm>  // min 등 알고리즘 함수 제공.
// using namespace std;  // std 이름 공간을 생략해 사용. ;는 문장 끝.
// 
// int solution(int n, int m, vector<vector<int>> edge_list, int k, vector<int> gps_log) {  // int는 정수, 중첩 vector는 도로 표. {}는 함수 영역.
//     vector<vector<int>> graph(n + 1);  // 거점별 인접 리스트 생성.
//     for (auto edge : edge_list) {  // auto는 타입 추론. 범위 for로 도로 순회.
//         graph[edge[0]].push_back(edge[1]);  // []는 인덱스, push_back은 배열 끝에 추가.
//         graph[edge[1]].push_back(edge[0]);  // 반대 방향 도로도 추가.
//     }  // 도로 반복 종료.
//     const int INF = 1000000000;  // const는 변경 금지 상수. 도달 불가 비용.
//     vector<int> dp(n + 1, INF);  // 거점별 비용을 불가능으로 초기화.
//     dp[gps_log[0]] = 0;  // 원래 시작 거점만 비용 0.
//     for (int time = 1; time < k; ++time) {  // 두 번째 시각부터 처리. ++는 1 증가.
//         vector<int> next_dp(n + 1, INF);  // 다음 시각 비용을 따로 계산.
//         for (int node = 1; node <= n; ++node) {  // 모든 도착 거점 후보 순회.
//             int best = dp[node];  // 현재 거점에 머무는 경우.
//             for (int neighbor : graph[node]) best = min(best, dp[neighbor]);  // 인접 거점에서 오는 경우와 비교해 최소 비용 선택.
//             next_dp[node] = best + (node != gps_log[time]);  // !=는 다름. 참이면 1을 더해 기록 수정 표시.
//         }  // 거점 반복 종료.
//         dp.swap(next_dp);  // swap은 두 배열 내용 교환. 완성한 다음 시각 비용을 현재 비용으로 사용.
//     }  // 시간 반복 종료.
//     int answer = dp[gps_log.back()];  // back은 마지막 원소. 원래 도착 거점 비용 조회.
//     return answer < INF ? answer : -1;  // 조건 ? 참일 때 : 거짓일 때. 불가능하면 -1 반환.
// }  // 정답 함수 종료.

// 풀이 요약
// dp[v]는 현재 시각에 v에 있을 때 필요한 최소 GPS 수정 횟수다. 직전 시각에 같은 거점에 머물거나 인접 거점에서 이동한 경우 중 최소를 선택한다.
// 시작 거점만 비용 0으로 초기화하고 마지막에는 원래 도착 거점의 값만 반환해 양 끝을 고정한다. 기록과 현재 거점이 다르면 수정 비용 1을 더한다.
// 예제 [1,2,3,3,6,7]은 네 번째 3을 5로 바꿔 한 번 수정한다. 시간 O(K(N+M)), 공간 O(N+M).
// 