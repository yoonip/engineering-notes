# 등대

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/133500) · Level 3 · C++

## 풀이

트리를 부모 순서로 펼친 뒤 자식부터 거꾸로 등대를 켠 상태와 끈 상태의 최소 점등 수 합치기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> lighthouse) {
    vector<vector<int>> graph(n + 1);
    for (const auto& edge : lighthouse) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }
    vector<int> parent(n + 1, 0), order{1};
    for (int i = 0; i < (int)order.size(); ++i) { int node = order[i]; for (int next : graph[node]) if (next != parent[node]) { parent[next] = node; order.push_back(next); } }
    vector<int> off(n + 1, 0), on(n + 1, 1);
    for (int i = (int)order.size() - 1; i > 0; --i) {
        int node = order[i], p = parent[node];
        off[p] += on[node];
        on[p] += min(off[node], on[node]);
    }
    return min(off[1], on[1]);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> lighthouse) {  // 부모·자식 간선을 덮는 최소 점등 수 계산
// vector<vector<int>> graph(n + 1);  // 등대 연결 트리의 인접 리스트 만들기
// for (const auto& edge : lighthouse) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }  // 간선을 양방향으로 등록
// vector<int> parent(n + 1, 0), order{1};  // 부모 배열과 루트부터의 순회 순서 저장
// for (int i = 0; i < (int)order.size(); ++i) { int node = order[i]; for (int next : graph[node]) if (next != parent[node]) { parent[next] = node; order.push_back(next); } }  // 재귀 없이 부모와 자식 관계 정하기
// vector<int> off(n + 1, 0), on(n + 1, 1);  // 각 등대를 끄거나 켠 상태의 최소 점등 수
// for (int i = (int)order.size() - 1; i > 0; --i) {  // 자식에서 부모 순서로 상태 합치기
// int node = order[i], p = parent[node];  // 현재 자식과 부모 읽기
// off[p] += on[node];  // 부모를 끄면 자식은 반드시 켜기
// on[p] += min(off[node], on[node]);  // 부모를 켜면 자식의 두 상태 중 작은 것 고르기
// }  // 블록 끝
// return min(off[1], on[1]);  // 루트의 두 상태 중 최소 점등 수 반환
// }  // 블록 끝

// 풀이 요약
// 트리를 부모 순서로 펼친 뒤 자식부터 거꾸로 등대를 켠 상태와 끈 상태의 최소 점등 수 합치기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:29
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/025_133500_%EB%93%B1%EB%8C%80/README.md)
