# 중요한 도로 — C++

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/214293?language=cpp)

레벨 5 · C++

## 풀이 요약

1번과 n번에서 다익스트라를 한 번씩 실행해 현재 최단 시간 D와 양끝 거리 계산

교통량을 0으로 내렸을 때 dist1[u]+L+distN[v] 또는 반대 방향이 D보다 작으면 감소에 민감한 도로

현재 최단 경로에 속하는 도로만 모은 부분 그래프에서 단절선을 찾으면 증가에 민감한 도로

모든 부분 그래프 도로는 실제 최단 경로에 들어가고 길이가 양수이므로, 단절선과 모든 최단 경로가 지나는 도로가 일치

두 조건 중 하나라도 만족하는 도로 번호를 오름차순으로 반환하고 없으면 [-1]

거리 합은 long long, DFS는 반복 스택 사용; 정점 N·도로 M에 대해 시간 O((N+M) log N), 공간 O(N+M)

## 코드와 줄별 설명

[제출 코드](solution.cpp) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~cpp
#include <algorithm>
#include <functional>
#include <limits>
#include <queue>
#include <utility>
#include <vector>

using namespace std;

struct Edge { int to, id; long long weight; };

static vector<long long> shortest(int start, const vector<vector<Edge>>& graph) {
    vector<long long> distance(graph.size(), numeric_limits<long long>::max() / 4);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> heap;
    distance[start] = 0;
    heap.push({0, start});
    while (!heap.empty()) {
        auto [cost, node] = heap.top(); heap.pop();
        if (cost != distance[node]) continue;
        for (const Edge& edge : graph[node]) {
            long long candidate = cost + edge.weight;
            if (candidate < distance[edge.to]) {
                distance[edge.to] = candidate;
                heap.push({candidate, edge.to});
            }
        }
    }
    return distance;
}

vector<int> solution(int n, vector<vector<int>> roads) {
    int m = static_cast<int>(roads.size());
    vector<vector<Edge>> graph(n + 1);
    for (int id = 0; id < m; ++id) {
        int u = roads[id][0], v = roads[id][1];
        long long weight = static_cast<long long>(roads[id][2]) + roads[id][3];
        graph[u].push_back({v, id, weight});
        graph[v].push_back({u, id, weight});
    }
    vector<long long> from = shortest(1, graph), to = shortest(n, graph);
    long long best = from[n];
    vector<bool> on_path(m, false), important(m, false);
    for (int id = 0; id < m; ++id) {
        int u = roads[id][0], v = roads[id][1];
        long long length = roads[id][2], weight = length + roads[id][3];
        important[id] = from[u] + length + to[v] < best || from[v] + length + to[u] < best;
        on_path[id] = from[u] + weight + to[v] == best || from[v] + weight + to[u] == best;
    }
    vector<int> entered(n + 1, 0), low(n + 1), parent(n + 1, 0), parent_edge(n + 1, -1);
    vector<size_t> next_arc(n + 1, 0);
    vector<int> stack{1};
    int timer = 1;
    entered[1] = low[1] = timer;
    while (!stack.empty()) {
        int node = stack.back();
        while (next_arc[node] < graph[node].size() && !on_path[graph[node][next_arc[node]].id]) ++next_arc[node];
        if (next_arc[node] == graph[node].size()) {
            stack.pop_back();
            int p = parent[node];
            if (p) {
                if (low[node] > entered[p]) important[parent_edge[node]] = true;
                low[p] = min(low[p], low[node]);
            }
            continue;
        }
        const Edge& edge = graph[node][next_arc[node]++];
        if (edge.id == parent_edge[node]) continue;
        int next = edge.to;
        if (!entered[next]) {
            parent[next] = node; parent_edge[next] = edge.id;
            entered[next] = low[next] = ++timer;
            stack.push_back(next);
        } else low[node] = min(low[node], entered[next]);
    }
    vector<int> answer;
    for (int id = 0; id < m; ++id) if (important[id]) answer.push_back(id + 1);
    if (answer.empty()) answer.push_back(-1);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // low 값의 최솟값 비교
// #include <functional>  // priority_queue를 최소 힙으로 만드는 greater
// #include <limits>  // 초기 최단 거리의 큰 long long 값
// #include <queue>  // 다익스트라에서 최소 거리 상태를 꺼낼 우선순위 큐
// #include <utility>  // 거리와 정점을 묶는 pair
// #include <vector>  // 인접 도로와 최단 거리·반복 DFS 상태 저장
// 
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// 
// struct Edge { int to, id; long long weight; };  // 도착 정점·원래 도로 번호·통과 시간을 한 간선에 보관
// 
// static vector<long long> shortest(int start, const vector<vector<Edge>>& graph) {  // 한 출발점에서 모든 정점까지 다익스트라 최단 거리 계산
//     vector<long long> distance(graph.size(), numeric_limits<long long>::max() / 4);  // 아직 도달하지 않은 정점 거리를 충분히 큰 값으로 초기화
//     priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> heap;  // 도착 시간이 작은 상태부터 꺼낼 최소 힙
//     distance[start] = 0;  // 출발점까지 거리는 0
//     heap.push({0, start});  // 출발점을 첫 탐색 상태로 추가
//     while (!heap.empty()) {  // 최소 거리 후보가 남아 있는 동안 탐색
//         auto [cost, node] = heap.top(); heap.pop();  // 가장 작은 거리의 정점 상태 꺼내기
//         if (cost != distance[node]) continue;  // 더 좋은 경로가 이미 나온 오래된 힙 상태는 제외
//         for (const Edge& edge : graph[node]) {  // 현재 정점의 모든 인접 도로 확인
//             long long candidate = cost + edge.weight;  // 이 도로를 지난 새 도착 시간
//             if (candidate < distance[edge.to]) {  // 기존 최단 시간보다 작을 때만 갱신
//                 distance[edge.to] = candidate;  // 이웃 정점의 새 최단 시간 저장
//                 heap.push({candidate, edge.to});  // 더 짧아진 상태를 최소 힙에 추가
//             }  // 현재 도로의 거리 완화 끝
//         }  // 현재 정점의 도로 확인 끝
//     }  // 모든 최단 거리 확정
//     return distance;  // 출발점 기준 거리 배열 반환
// }  // 한 출발점의 다익스트라 끝
// 
// vector<int> solution(int n, vector<vector<int>> roads) {  // 교통량 하나의 변화가 최단 도착 시간을 바꿀 수 있는 도로 번호 찾기
//     int m = static_cast<int>(roads.size());  // 원래 도로 개수
//     vector<vector<Edge>> graph(n + 1);  // 정점별 양방향 인접 도로 목록
//     for (int id = 0; id < m; ++id) {  // 입력 순서대로 도로를 인접 목록에 등록
//         int u = roads[id][0], v = roads[id][1];  // 이번 도로의 양 끝 정점
//         long long weight = static_cast<long long>(roads[id][2]) + roads[id][3];  // 길이와 교통량을 더한 실제 통과 시간
//         graph[u].push_back({v, id, weight});  // U에서 V로 가는 도로 등록
//         graph[v].push_back({u, id, weight});  // 같은 도로 번호로 V에서 U로 가는 방향도 등록
//     }  // 원래 도로의 양방향 그래프 구성 끝
//     vector<long long> from = shortest(1, graph), to = shortest(n, graph);  // 출발지와 목적지 양끝에서의 최단 거리 계산
//     long long best = from[n];  // 현재 교통량에서의 가장 빠른 도착 시간
//     vector<bool> on_path(m, false), important(m, false);  // 최단 경로에 속한 도로와 교통량 변화에 민감한 도로 표시
//     for (int id = 0; id < m; ++id) {  // 도로별로 감소 가능성과 최단 경로 포함 여부 판정
//         int u = roads[id][0], v = roads[id][1];  // 이번 도로의 양 끝 정점
//         long long length = roads[id][2], weight = length + roads[id][3];  // 교통량 0일 때의 최소 시간과 현재 시간
//         important[id] = from[u] + length + to[v] < best || from[v] + length + to[u] < best;  // 교통량을 0으로 줄여 기존 최단 시간보다 빨라질 수 있는지 양방향 검사
//         on_path[id] = from[u] + weight + to[v] == best || from[v] + weight + to[u] == best;  // 이 도로를 지나는 현재 최단 경로가 하나라도 있는지 표시
//     }  // 교통량 감소에 민감한 도로와 최단 경로 부분 그래프 준비 끝
//     vector<int> entered(n + 1, 0), low(n + 1), parent(n + 1, 0), parent_edge(n + 1, -1);  // 단절선 DFS의 방문 순서·최소 도달 순서·부모 정점과 도로
//     vector<size_t> next_arc(n + 1, 0);  // 각 정점에서 다음에 확인할 인접 도로 위치
//     vector<int> stack{1};  // 재귀 대신 DFS 경로를 저장하고 출발지부터 시작
//     int timer = 1;  // DFS 방문 순서 번호
//     entered[1] = low[1] = timer;  // 출발지의 방문 순서와 최소 도달 순서를 1로 설정
//     while (!stack.empty()) {  // 반복 DFS로 최단 경로 부분 그래프의 단절선 찾기
//         int node = stack.back();  // 아직 자식 검사가 끝나지 않은 현재 정점
//         while (next_arc[node] < graph[node].size() && !on_path[graph[node][next_arc[node]].id]) ++next_arc[node];  // 현재 최단 경로에 쓰이지 않는 도로는 제외
//         if (next_arc[node] == graph[node].size()) {  // 모든 인접 도로 검사를 마쳤으면 부모로 돌아가기
//             stack.pop_back();  // 현재 정점을 DFS 스택에서 제거
//             int p = parent[node];  // 현재 서브트리 결과를 전달할 부모
//             if (p) {  // 출발지 외 정점에서만 부모 도로를 검사
//                 if (low[node] > entered[p]) important[parent_edge[node]] = true;  // 우회 연결이 없는 단절선은 모든 최단 경로가 지나므로 증가에 민감
//                 low[p] = min(low[p], low[node]);  // 자식 쪽에서 도달한 가장 이른 방문 순서를 부모에 반영
//             }  // 부모 도로의 단절선 판정 끝
//             continue;  // 부모 정점의 남은 도로 검사로 복귀
//         }  // 완료 정점을 되돌리는 처리 끝
//         const Edge& edge = graph[node][next_arc[node]++];  // 현재 도로를 고르고 다음에 볼 위치를 한 칸 이동
//         if (edge.id == parent_edge[node]) continue;  // 방금 내려온 부모 도로는 역방향 우회로로 세지 않음
//         int next = edge.to;  // 이번 도로의 이웃 정점
//         if (!entered[next]) {  // 처음 만난 이웃이면 DFS 자식으로 내려가기
//             parent[next] = node; parent_edge[next] = edge.id;  // 돌아올 부모 정점과 도로 번호 기록
//             entered[next] = low[next] = ++timer;  // 새 방문 순서를 주고 최소 도달 순서도 같은 값으로 시작
//             stack.push_back(next);  // 자식을 DFS 스택에 넣어 그 서브트리부터 처리
//         } else low[node] = min(low[node], entered[next]);  // 이미 본 정점으로의 우회 연결은 최소 도달 순서에 반영
//     }  // 현재 최단 경로를 모두 지나는 도로 표시 끝
//     vector<int> answer;  // 중요한 도로 번호를 담을 반환 배열
//     for (int id = 0; id < m; ++id) if (important[id]) answer.push_back(id + 1);  // 원래 도로 번호를 작은 순서대로 결과에 추가
//     if (answer.empty()) answer.push_back(-1);  // 교통량 변화에 민감한 도로가 없으면 -1 한 개 반환
//     return answer;  // 오름차순 도로 번호 배열 반환
// }  // 중요한 도로 계산 끝

// 풀이 요약
// 1번과 n번에서 다익스트라를 한 번씩 실행해 현재 최단 시간 D와 양끝 거리 계산
// 교통량을 0으로 내렸을 때 dist1[u]+L+distN[v] 또는 반대 방향이 D보다 작으면 감소에 민감한 도로
// 현재 최단 경로에 속하는 도로만 모은 부분 그래프에서 단절선을 찾으면 증가에 민감한 도로
// 모든 부분 그래프 도로는 실제 최단 경로에 들어가고 길이가 양수이므로, 단절선과 모든 최단 경로가 지나는 도로가 일치
// 두 조건 중 하나라도 만족하는 도로 번호를 오름차순으로 반환하고 없으면 [-1]
// 거리 합은 long long, DFS는 반복 스택 사용; 정점 N·도로 M에 대해 시간 O((N+M) log N), 공간 O(N+M)
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C++ 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
