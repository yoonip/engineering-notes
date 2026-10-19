// vector는 가변 길이 배열.
#include <vector>
// min 등 알고리즘 함수 제공.
#include <algorithm>
using namespace std;

// {}는 함수 영역.
int solution(int n, int m, vector<vector<int>> edge_list, int k, vector<int> gps_log) {
    // 거점별 인접 리스트 생성.
    vector<vector<int>> graph(n + 1);
    // 범위 for로 도로 순회.
    for (auto edge : edge_list) {
        // []는 인덱스, push_back은 배열 끝에 추가.
        graph[edge[0]].push_back(edge[1]);
        // 반대 방향 도로도 추가.
        graph[edge[1]].push_back(edge[0]);
    }
    // 도달 불가 비용.
    const int INF = 1000000000;
    // 거점별 비용을 불가능으로 초기화.
    vector<int> dp(n + 1, INF);
    // 원래 시작 거점만 비용 0.
    dp[gps_log[0]] = 0;
    // ++는 1 증가.
    for (int time = 1; time < k; ++time) {
        // 다음 시각 비용을 따로 계산.
        vector<int> next_dp(n + 1, INF);
        // 모든 도착 거점 후보 순회.
        for (int node = 1; node <= n; ++node) {
            // 현재 거점에 머무는 경우.
            int best = dp[node];
            // 인접 거점에서 오는 경우와 비교해 최소 비용 선택.
            for (int neighbor : graph[node]) best = min(best, dp[neighbor]);
            // 참이면 1을 더해 기록 수정 표시.
            next_dp[node] = best + (node != gps_log[time]);
        }
        // 완성한 다음 시각 비용을 현재 비용으로 사용.
        dp.swap(next_dp);
    }
    // 원래 도착 거점 비용 조회.
    int answer = dp[gps_log.back()];
    // 불가능하면 -1 반환.
    return answer < INF ? answer : -1;
}
