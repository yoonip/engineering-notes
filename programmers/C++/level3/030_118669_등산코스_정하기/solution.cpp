#include <algorithm>
#include <functional>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(int n, vector<vector<int>> paths, vector<int> gates, vector<int> summits) {
    vector<vector<pair<int, int>>> graph(n + 1);
    for (const auto& path : paths) { graph[path[0]].push_back({path[1], path[2]}); graph[path[1]].push_back({path[0], path[2]}); }
    vector<bool> is_summit(n + 1, false); for (int summit : summits) is_summit[summit] = true;
    vector<int> intensity(n + 1, 1000000000); priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> heap;
    for (int gate : gates) { intensity[gate] = 0; heap.push({0, gate}); }
    while (!heap.empty()) {
        auto [current, node] = heap.top(); heap.pop();
        if (current != intensity[node] || is_summit[node]) continue;
        for (auto [next, time] : graph[node]) {
            int candidate = max(current, time);
            if (candidate < intensity[next]) { intensity[next] = candidate; heap.push({candidate, next}); }
        }
    }
    int best = *min_element(summits.begin(), summits.end(), [&](int a, int b) { return intensity[a] != intensity[b] ? intensity[a] < intensity[b] : a < b; });
    return {best, intensity[best]};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, vector<vector<int>> paths, vector<int> gates, vector<int> summits) {  // 출입구부터 최소 intensity로 정상까지 탐색
// vector<vector<pair<int, int>>> graph(n + 1);  // 등산 경로와 이동 시간 저장
// for (const auto& path : paths) { graph[path[0]].push_back({path[1], path[2]}); graph[path[1]].push_back({path[0], path[2]}); }  // 경로를 양방향 간선으로 등록
// vector<bool> is_summit(n + 1, false); for (int summit : summits) is_summit[summit] = true;  // 정상 도착 후에는 더 진행하지 않도록 표시
// vector<int> intensity(n + 1, 1000000000); priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> heap;  // 지점별 최소 intensity와 탐색 힙 만들기
// for (int gate : gates) { intensity[gate] = 0; heap.push({0, gate}); }  // 모든 출입구에서 동시에 탐색을 시작
// while (!heap.empty()) {  // intensity가 작은 상태부터 처리
// auto [current, node] = heap.top(); heap.pop();  // 현재 최선 후보 꺼내기
// if (current != intensity[node] || is_summit[node]) continue;  // 오래된 상태나 정상에서는 확장을 멈추기
// for (auto [next, time] : graph[node]) {  // 인접 지점으로 이동할 때의 intensity 계산
// int candidate = max(current, time);  // 지나온 간선 중 최대 시간 유지
// if (candidate < intensity[next]) { intensity[next] = candidate; heap.push({candidate, next}); }  // 더 낮은 intensity 경로이면 갱신
// }  // 블록 끝
// }  // 블록 끝
// int best = *min_element(summits.begin(), summits.end(), [&](int a, int b) { return intensity[a] != intensity[b] ? intensity[a] < intensity[b] : a < b; });  // 최소 intensity와 작은 정상 번호 순서로 선택
// return {best, intensity[best]};  // 정상 번호와 해당 intensity 반환
// }  // 블록 끝

// 풀이 요약
// 모든 출입구에서 동시에 최소 intensity 경로를 탐색하고 정상에서는 확장하지 않으며 최소 intensity와 작은 정상 번호 선택
