# 가장 먼 노드

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49189) · Level 3 · C++

## 풀이

1번 정점에서 너비 우선 탐색으로 최단 거리를 구하고 가장 큰 거리를 가진 정점 수 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <queue>
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> edge) {
    vector<vector<int>> graph(n + 1);
    for (const auto& e : edge) { graph[e[0]].push_back(e[1]); graph[e[1]].push_back(e[0]); }
    vector<int> distance(n + 1, -1); queue<int> q; distance[1] = 0; q.push(1);
    while (!q.empty()) { int node = q.front(); q.pop(); for (int next : graph[node]) if (distance[next] == -1) { distance[next] = distance[node] + 1; q.push(next); } }
    int farthest = *max_element(distance.begin(), distance.end());
    return (int)count(distance.begin(), distance.end(), farthest);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> edge) {  // 1번에서 가장 멀리 떨어진 정점 개수 계산
// vector<vector<int>> graph(n + 1);  // 무방향 그래프의 인접 리스트 만들기
// for (const auto& e : edge) { graph[e[0]].push_back(e[1]); graph[e[1]].push_back(e[0]); }  // 모든 간선을 양방향으로 등록
// vector<int> distance(n + 1, -1); queue<int> q; distance[1] = 0; q.push(1);  // 1번 정점에서 너비 우선 탐색을 시작
// while (!q.empty()) { int node = q.front(); q.pop(); for (int next : graph[node]) if (distance[next] == -1) { distance[next] = distance[node] + 1; q.push(next); } }  // 각 정점의 최단 간선 수 구하기
// int farthest = *max_element(distance.begin(), distance.end());  // 가장 먼 정점까지의 거리 구하기
// return (int)count(distance.begin(), distance.end(), farthest);  // 최대 거리를 가진 정점 수 반환
// }  // 블록 끝

// 풀이 요약
// 1번 정점에서 너비 우선 탐색으로 최단 거리를 구하고 가장 큰 거리를 가진 정점 수 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/057_49189_%EA%B0%80%EC%9E%A5_%EB%A8%BC_%EB%85%B8%EB%93%9C/README.md)
