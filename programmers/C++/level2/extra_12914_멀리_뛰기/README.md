# 멀리 뛰기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12914) · Level 2 · C++

## 풀이

마지막에 한 칸 또는 두 칸 뛰는 두 경우의 수를 이전 두 길이의 점화식으로 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
long long solution(int n) {
    long long previous = 1, current = 1;
    for (int i = 2; i <= n; ++i) {
        long long next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return current;
}

// 전체 코드 줄별 설명
// long long solution(int n) {  // 마지막 한 칸·두 칸 점프의 경우의 수 합치기
// long long previous = 1, current = 1;  // 길이 0과 1을 이동하는 방법 수 초기화
// for (int i = 2; i <= n; ++i) {  // 마지막에 한 칸 또는 두 칸 뛰는 두 경우 합치기
// long long next = (previous + current) % 1234567;  // 이전 두 길이의 방법 수를 더해 나머지 구하기
// previous = current; current = next;  // 연속한 두 길이의 방법 수 갱신
// }  // 블록 끝
// return current;  // n칸을 이동하는 방법 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 마지막에 한 칸 또는 두 칸 뛰는 두 경우의 수를 이전 두 길이의 점화식으로 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:40:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/extra_12914_%EB%A9%80%EB%A6%AC_%EB%9B%B0%EA%B8%B0/README.md)
