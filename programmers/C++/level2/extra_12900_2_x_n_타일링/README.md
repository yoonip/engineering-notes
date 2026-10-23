# 2 x n 타일링

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12900) · Level 2 · C++

## 풀이

마지막 타일 배치에 따라 이전 두 너비의 타일링 수를 더하는 점화식 적용

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int n) {
    const int MOD = 1000000007;
    int previous = 1, current = 1;
    for (int width = 2; width <= n; ++width) {
        int next = (previous + current) % MOD;
        previous = current; current = next;
    }
    return current;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 마지막 배치 두 경우로 2행 타일링 수 계산
// const int MOD = 1000000007;  // 결과의 나머지 기준 선언
// int previous = 1, current = 1;  // 너비 0과 1의 타일링 수 초기화
// for (int width = 2; width <= n; ++width) {  // 마지막에 세로 한 개 또는 가로 두 개를 두는 경우 합치기
// int next = (previous + current) % MOD;  // 이전 두 너비의 경우의 수를 더하기
// previous = current; current = next;  // 연속한 두 너비의 값 갱신
// }  // 블록 끝
// return current;  // 2×n 타일링 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 마지막 타일 배치에 따라 이전 두 너비의 타일링 수를 더하는 점화식 적용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12900_2_x_n_%ED%83%80%EC%9D%BC%EB%A7%81/README.md)
