# 숫자 변환하기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/154538) · Level 2 · C++

## 풀이

정수 x에서 허용된 세 연산을 간선으로 보고 너비 우선 탐색으로 y까지의 최소 연산 수 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <queue>
#include <vector>
using namespace std;

int solution(int x, int y, int n) {
    vector<int> distance(y + 1, -1);
    queue<int> q;
    distance[x] = 0; q.push(x);
    while (!q.empty()) {
        int value = q.front(); q.pop();
        if (value == y) return distance[value];
        for (int next : {value + n, value * 2, value * 3}) {
            if (next <= y && distance[next] == -1) {
                distance[next] = distance[value] + 1;
                q.push(next);
            }
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int x, int y, int n) {  // 허용 연산으로 x에서 y까지 가는 최소 횟수
// vector<int> distance(y + 1, -1);  // y 이하 정수의 최소 연산 수 저장
// queue<int> q;  // 너비 우선 탐색 큐 선언
// distance[x] = 0; q.push(x);  // 시작값을 연산 수 0으로 등록
// while (!q.empty()) {  // 연산 수가 적은 상태부터 처리
// int value = q.front(); q.pop();  // 현재 정수를 큐에서 꺼내기
// if (value == y) return distance[value];  // y에 처음 도착하면 최소 횟수 반환
// for (int next : {value + n, value * 2, value * 3}) {  // 허용된 세 연산의 결과를 차례대로 검사
// if (next <= y && distance[next] == -1) {  // 범위 안의 새 상태만 처리
// distance[next] = distance[value] + 1;  // 연산 한 번을 거리로 기록
// q.push(next);  // 새 상태를 큐에 넣기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// return -1;  // y로 바꿀 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 정수 x에서 허용된 세 연산을 간선으로 보고 너비 우선 탐색으로 y까지의 최소 연산 수 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:32:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/026_154538_%EC%88%AB%EC%9E%90_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0/README.md)
