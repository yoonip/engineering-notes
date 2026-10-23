# 디펜스 게임

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/142085) · Level 2 · C++

## 풀이

현재까지 큰 k개 라운드를 무적권 후보로 유지하고 나머지 작은 라운드부터 병사로 처리

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <functional>
#include <queue>
#include <vector>
using namespace std;

int solution(int n, int k, vector<int> enemy) {
    priority_queue<int, vector<int>, greater<int>> shielded;
    for (int i = 0; i < (int)enemy.size(); ++i) {
        shielded.push(enemy[i]);
        if ((int)shielded.size() > k) { n -= shielded.top(); shielded.pop(); }
        if (n < 0) return i;
    }
    return (int)enemy.size();
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, int k, vector<int> enemy) {  // 가장 큰 k개 공격을 무적권으로 남기기
// priority_queue<int, vector<int>, greater<int>> shielded;  // 무적권으로 막을 후보를 최소 힙으로 관리
// for (int i = 0; i < (int)enemy.size(); ++i) {  // 적의 라운드를 순서대로 처리
// shielded.push(enemy[i]);  // 현재 라운드를 무적권 후보에 넣기
// if ((int)shielded.size() > k) { n -= shielded.top(); shielded.pop(); }  // 후보가 k개를 넘으면 가장 작은 라운드를 병사로 막기
// if (n < 0) return i;  // 병사가 부족하면 완료한 라운드 수 반환
// }  // 블록 끝
// return (int)enemy.size();  // 모든 라운드를 막았으면 전체 수 반환
// }  // 블록 끝

// 풀이 요약
// 현재까지 큰 k개 라운드를 무적권 후보로 유지하고 나머지 작은 라운드부터 병사로 처리
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:33:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/033_142085_%EB%94%94%ED%8E%9C%EC%8A%A4_%EA%B2%8C%EC%9E%84/README.md)
