# 피보나치 수

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12945) · Level 2 · C++

## 풀이

연속한 두 피보나치 항만 유지하며 합의 나머지를 다음 항으로 계산

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int n) {
    int previous = 0, current = 1;
    for (int i = 0; i < n; ++i) {
        int next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return previous;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 이전 두 피보나치 값만 남기며 다음 항 계산
// int previous = 0, current = 1;  // F(0)과 F(1)을 초기값으로 두기
// for (int i = 0; i < n; ++i) {  // 피보나치 항을 n번 앞으로 이동
// int next = (previous + current) % 1234567;  // 두 항의 합을 나머지로 줄여 다음 항 구하기
// previous = current; current = next;  // 연속한 두 항을 다음 위치로 갱신
// }  // 블록 끝
// return previous;  // F(n)의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 연속한 두 피보나치 항만 유지하며 합의 나머지를 다음 항으로 계산
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12945_%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98_%EC%88%98/README.md)
