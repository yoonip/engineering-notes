# 모두 0으로 만들기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/76503) · Level 3 · C++

## 풀이

총 무게가 0인지 확인하고 트리의 자식부터 무게를 부모로 모두 옮기며 이동 절댓값을 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <cstdlib>
#include <numeric>
#include <vector>
using namespace std;

long long solution(vector<int> a, vector<vector<int>> edges) {
    if (accumulate(a.begin(), a.end(), 0LL) != 0) return -1;
    int n = (int)a.size(); vector<vector<int>> graph(n);
    for (const auto& edge : edges) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }
    vector<int> parent(n, -1), order{0};
    for (int i = 0; i < (int)order.size(); ++i) { int node = order[i]; for (int next : graph[node]) if (next != parent[node]) { parent[next] = node; order.push_back(next); } }
    vector<long long> weight(a.begin(), a.end()); long long answer = 0;
    for (int i = (int)order.size() - 1; i > 0; --i) { int node = order[i]; answer += llabs(weight[node]); weight[parent[node]] += weight[node]; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(vector<int> a, vector<vector<int>> edges) {  // 자식부터 가중치를 부모로 보내 이동량 합산
// if (accumulate(a.begin(), a.end(), 0LL) != 0) return -1;  // 총 무게가 0이 아니면 모든 정점을 0으로 만들 수 없음
// int n = (int)a.size(); vector<vector<int>> graph(n);  // 트리의 인접 리스트 만들기
// for (const auto& edge : edges) { graph[edge[0]].push_back(edge[1]); graph[edge[1]].push_back(edge[0]); }  // 간선을 양방향으로 등록
// vector<int> parent(n, -1), order{0};  // 부모 배열과 루트부터의 순회 순서 저장
// for (int i = 0; i < (int)order.size(); ++i) { int node = order[i]; for (int next : graph[node]) if (next != parent[node]) { parent[next] = node; order.push_back(next); } }  // 재귀 없이 자식 순서 정하기
// vector<long long> weight(a.begin(), a.end()); long long answer = 0;  // 누적 무게와 총 이동 비용을 넓은 정수형으로 저장
// for (int i = (int)order.size() - 1; i > 0; --i) { int node = order[i]; answer += llabs(weight[node]); weight[parent[node]] += weight[node]; }  // 자식의 무게를 부모로 모두 옮기며 절댓값 비용을 더하기
// return answer;  // 모든 무게를 0으로 만드는 최소 비용 반환
// }  // 블록 끝

// 풀이 요약
// 총 무게가 0인지 확인하고 트리의 자식부터 무게를 부모로 모두 옮기며 이동 절댓값을 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:45
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/042_76503_%EB%AA%A8%EB%91%90_0%EC%9C%BC%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
