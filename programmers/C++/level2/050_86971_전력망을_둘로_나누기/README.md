# 전력망을 둘로 나누기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86971) · Level 2 · C++

## 풀이

트리의 자식 서브트리 크기를 구해 해당 전선을 끊을 때의 두 부분 크기 차이 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cstdlib>
#include <functional>
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> wires) {
    vector<vector<int>> graph(n + 1);
    for (const auto& wire : wires) { graph[wire[0]].push_back(wire[1]); graph[wire[1]].push_back(wire[0]); }
    int answer = n;
    function<int(int, int)> dfs = [&](int node, int parent) {
        int size = 1;
        for (int next : graph[node]) if (next != parent) {
            int child = dfs(next, node);
            answer = min(answer, abs(n - 2 * child));
            size += child;
        }
        return size;
    };
    dfs(1, 0);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> wires) {  // 각 전선을 끊을 때 두 서브트리의 크기 차이 비교
// vector<vector<int>> graph(n + 1);  // 송전탑의 인접 리스트 만들기
// for (const auto& wire : wires) { graph[wire[0]].push_back(wire[1]); graph[wire[1]].push_back(wire[0]); }  // 전선을 양방향으로 등록
// int answer = n;  // 두 전력망의 최소 크기 차이 초기화
// function<int(int, int)> dfs = [&](int node, int parent) {  // 현재 서브트리의 정점 수 구하기
// int size = 1;  // 현재 송전탑 자체 세기
// for (int next : graph[node]) if (next != parent) {  // 부모를 제외한 자식 서브트리 처리
// int child = dfs(next, node);  // 자식 쪽 전력망의 크기 구하기
// answer = min(answer, abs(n - 2 * child));  // 해당 전선을 끊을 때 두 부분의 크기 차이 비교
// size += child;  // 현재 서브트리 크기에 자식 크기를 더하기
// }  // 블록 끝
// return size;  // 현재 서브트리의 크기 반환
// };  // 블록 끝
// dfs(1, 0);  // 1번 송전탑을 기준으로 트리를 순회
// return answer;  // 전선 하나를 끊을 때 가능한 최소 차이 반환
// }  // 블록 끝

// 풀이 요약
// 트리의 자식 서브트리 크기를 구해 해당 전선을 끊을 때의 두 부분 크기 차이 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:38:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/050_86971_%EC%A0%84%EB%A0%A5%EB%A7%9D%EC%9D%84_%EB%91%98%EB%A1%9C_%EB%82%98%EB%88%84%EA%B8%B0/README.md)
