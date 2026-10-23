# 택배 배달과 수거하기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150369) · Level 2 · C++

## 풀이

먼 집부터 배달과 수거의 누적 작업량을 계산하고 두 작업을 감당하는 왕복 횟수와 거리를 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

long long solution(int cap, int n, vector<int> deliveries, vector<int> pickups) {
    long long delivery = 0, pickup = 0, answer = 0;
    for (int index = n - 1; index >= 0; --index) {
        delivery += deliveries[index]; pickup += pickups[index];
        long long trips = max({0LL, (delivery + cap - 1) / cap, (pickup + cap - 1) / cap});
        answer += trips * (index + 1) * 2;
        delivery -= trips * cap; pickup -= trips * cap;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int cap, int n, vector<int> deliveries, vector<int> pickups) {  // 먼 집부터 배달과 수거 왕복 거리 누적
// long long delivery = 0, pickup = 0, answer = 0;  // 먼 집부터 누적한 작업량과 이동 거리 초기화
// for (int index = n - 1; index >= 0; --index) {  // 가장 먼 집부터 가까운 집으로 처리
// delivery += deliveries[index]; pickup += pickups[index];  // 현재 위치의 배달과 수거량을 더하기
// long long trips = max({0LL, (delivery + cap - 1) / cap, (pickup + cap - 1) / cap});  // 두 작업을 모두 감당하는 최소 왕복 횟수를 올림 나눗셈으로 구하기
// answer += trips * (index + 1) * 2;  // 해당 집까지의 왕복 거리 누적
// delivery -= trips * cap; pickup -= trips * cap;  // 왕복으로 확보한 용량을 남은 작업량에서 빼기
// }  // 블록 끝
// return answer;  // 전체 최소 이동 거리 반환
// }  // 블록 끝

// 풀이 요약
// 먼 집부터 배달과 수거의 누적 작업량을 계산하고 두 작업을 감당하는 왕복 횟수와 거리를 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:32:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/028_150369_%ED%83%9D%EB%B0%B0_%EB%B0%B0%EB%8B%AC%EA%B3%BC_%EC%88%98%EA%B1%B0%ED%95%98%EA%B8%B0/README.md)
