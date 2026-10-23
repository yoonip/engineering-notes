# 도넛과 막대 그래프

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258711) · Level 2 · C++

## 풀이

생성 정점, 막대의 끝 정점, 8자의 교차 정점을 진입 및 진출 차수로 구분해 그래프별 개수 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

vector<int> solution(vector<vector<int>> edges) {
    int size = 1;
    for (const auto& edge : edges) size = max(size, max(edge[0], edge[1]) + 1);
    vector<int> incoming(size, 0), outgoing(size, 0);
    for (const auto& edge : edges) { ++outgoing[edge[0]]; ++incoming[edge[1]]; }
    int created = 0, sticks = 0, eights = 0;
    for (int node = 1; node < size; ++node) {
        if (incoming[node] == 0 && outgoing[node] >= 2) created = node;
        else if (outgoing[node] == 0 && incoming[node] > 0) ++sticks;
        else if (outgoing[node] == 2 && incoming[node] >= 2) ++eights;
    }
    return {created, outgoing[created] - sticks - eights, sticks, eights};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(vector<vector<int>> edges) {  // 차수로 생성 정점과 세 종류 그래프 구분
// int size = 1;  // 인덱스 배열에 필요한 크기 초기화
// for (const auto& edge : edges) size = max(size, max(edge[0], edge[1]) + 1);  // 가장 큰 정점 번호 다음까지 공간을 확보
// vector<int> incoming(size, 0), outgoing(size, 0);  // 정점별 진입 차수와 진출 차수 초기화
// for (const auto& edge : edges) { ++outgoing[edge[0]]; ++incoming[edge[1]]; }  // 간선 양 끝의 차수 세기
// int created = 0, sticks = 0, eights = 0;  // 생성 정점과 막대 및 8자 그래프 수 초기화
// for (int node = 1; node < size; ++node) {  // 모든 정점의 차수 특징 검사
// if (incoming[node] == 0 && outgoing[node] >= 2) created = node;  // 들어오는 간선 없이 둘 이상으로 나가면 생성 정점
// else if (outgoing[node] == 0 && incoming[node] > 0) ++sticks;  // 막대 끝 정점으로 막대 그래프 세기
// else if (outgoing[node] == 2 && incoming[node] >= 2) ++eights;  // 8자 그래프의 교차 정점으로 개수 세기
// }  // 블록 끝
// return {created, outgoing[created] - sticks - eights, sticks, eights};  // 전체 분기 수에서 막대와 8자를 빼 도넛 수를 구해 반환
// }  // 블록 끝

// 풀이 요약
// 생성 정점, 막대의 끝 정점, 8자의 교차 정점을 진입 및 진출 차수로 구분해 그래프별 개수 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:05
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/011_258711_%EB%8F%84%EB%84%9B%EA%B3%BC_%EB%A7%89%EB%8C%80_%EA%B7%B8%EB%9E%98%ED%94%84/README.md)
