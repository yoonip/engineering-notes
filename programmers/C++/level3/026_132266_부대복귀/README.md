# 부대복귀

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/132266) · Level 3 · C++

## 풀이

모든 부대원의 공통 목적지에서 한 번 너비 우선 탐색해 각 출발지의 최단 거리 읽기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <queue>
#include <vector>
using namespace std;

vector<int> solution(int n, vector<vector<int>> roads, vector<int> sources, int destination) {
    vector<vector<int>> graph(n + 1);
    for (const auto& edge : roads) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }
    vector<int> distance(n + 1, -1); queue<int> q; distance[destination] = 0; q.push(destination);
    while (!q.empty()) {
        int node = q.front(); q.pop();
        for (int next : graph[node]) if (distance[next] == -1) { distance[next] = distance[node] + 1; q.push(next); }
    }
    vector<int> answer; for (int source : sources) answer.push_back(distance[source]);
    return answer;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, vector<vector<int>> roads, vector<int> sources, int destination) {  // 목적지에서 한 번 탐색해 모든 출발 거리 구하기
// vector<vector<int>> graph(n + 1);  // 부대 지역의 양방향 도로 저장
// for (const auto& edge : roads) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }  // 인접 리스트에 간선 등록
// vector<int> distance(n + 1, -1); queue<int> q; distance[destination] = 0; q.push(destination);  // 목적지에서 역방향 너비 우선 탐색을 시작
// while (!q.empty()) {  // 목적지에서 가까운 지역부터 처리
// int node = q.front(); q.pop();  // 현재 지역을 큐에서 꺼내기
// for (int next : graph[node]) if (distance[next] == -1) { distance[next] = distance[node] + 1; q.push(next); }  // 미방문 이웃의 최단 거리 기록
// }  // 블록 끝
// vector<int> answer; for (int source : sources) answer.push_back(distance[source]);  // 각 부대원의 출발지에 해당하는 거리 읽기
// return answer;  // 복귀 시간 또는 도달 불가 -1 반환
// }  // 블록 끝

// 풀이 요약
// 모든 부대원의 공통 목적지에서 한 번 너비 우선 탐색해 각 출발지의 최단 거리 읽기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/026_132266_%EB%B6%80%EB%8C%80%EB%B3%B5%EA%B7%80/README.md)
