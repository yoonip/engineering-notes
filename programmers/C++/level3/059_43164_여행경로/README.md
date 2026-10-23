# 여행경로

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/43164) · Level 3 · C++

## 풀이

도착지를 역순 정렬해 작은 공항부터 간선을 사용하고 더 갈 수 없는 공항을 역순으로 확정하는 오일러 경로를 구성

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <map>
#include <string>
#include <vector>
using namespace std;

vector<string> solution(vector<vector<string>> tickets) {
    map<string,vector<string>> graph;
    for (const auto& ticket : tickets) graph[ticket[0]].push_back(ticket[1]);
    for (auto& entry : graph) sort(entry.second.rbegin(), entry.second.rend());
    vector<string> stack{"ICN"}, route;
    while (!stack.empty()) {
        auto& next = graph[stack.back()];
        if (!next.empty()) { string airport = next.back(); next.pop_back(); stack.push_back(airport); }
        else { route.push_back(stack.back()); stack.pop_back(); }
    }
    reverse(route.begin(), route.end());
    return route;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <map>  // 키를 정렬해 보관하는 map
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<vector<string>> tickets) {  // 모든 항공권을 사용하는 사전순 최소 경로 복원
// map<string,vector<string>> graph;  // 출발 공항별 도착 공항 목록 저장
// for (const auto& ticket : tickets) graph[ticket[0]].push_back(ticket[1]);  // 항공권을 방향 간선으로 등록
// for (auto& entry : graph) sort(entry.second.rbegin(), entry.second.rend());  // 끝에서 가장 작은 도착지를 꺼내도록 역순 정렬
// vector<string> stack{"ICN"}, route;  // 진행 중인 경로와 막힌 뒤 확정하는 역순 경로 저장
// while (!stack.empty()) {  // 모든 항공권을 사용하는 오일러 경로를 구성
// auto& next = graph[stack.back()];  // 현재 공항의 남은 항공권을 참조
// if (!next.empty()) { string airport = next.back(); next.pop_back(); stack.push_back(airport); }  // 가장 작은 도착지로 남은 간선을 하나 사용
// else { route.push_back(stack.back()); stack.pop_back(); }  // 더 갈 수 없으면 역순 경로에 현재 공항을 확정하기
// }  // 블록 끝
// reverse(route.begin(), route.end());  // 확정한 역순 경로를 실제 여행 순서로 바꾸기
// return route;  // 사전순으로 가장 빠른 전체 여행 경로 반환
// }  // 블록 끝

// 풀이 요약
// 도착지를 역순 정렬해 작은 공항부터 간선을 사용하고 더 갈 수 없는 공항을 역순으로 확정하는 오일러 경로를 구성
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/059_43164_%EC%97%AC%ED%96%89%EA%B2%BD%EB%A1%9C/README.md)
