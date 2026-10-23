# 올바른 괄호의 갯수

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12929) · Level 4 · C

## 풀이

모든 올바른 괄호 문자열은 유일하게 (내부 문자열)+뒤쪽 문자열로 나뉨; 내부·뒤쪽의 가능한 쌍 수별 곱을 모두 더하는 카탈란 수 DP
예: 2쌍은 (())와 ()() 두 가지, 3쌍은 다섯 가지
시간 O(n^2), 공간 O(n).; 이 문제는 나머지 연산 없이 실제 개수를 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int n) {
    long long* dp = calloc((size_t)n + 1, sizeof(*dp)); dp[0] = 1;
    for (int pairs = 1; pairs <= n; ++pairs) for (int inside = 0; inside < pairs; ++inside) dp[pairs] += dp[inside] * dp[pairs - 1 - inside];
    int answer = (int)dp[n]; free(dp);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int n) {  // 모든 올바른 괄호 문자열은 유일하게 (내부 문자열)+뒤쪽 문자열로 나뉨; 내부·뒤쪽의 가능한 쌍 수별 곱을 모두 더하는 카탈란 수 DP
//     long long* dp = calloc((size_t)n + 1, sizeof(*dp)); dp[0] = 1;  // 괄호 쌍 수별 올바른 문자열 수 공간 확보하고 0으로 시작
//     for (int pairs = 1; pairs <= n; ++pairs) for (int inside = 0; inside < pairs; ++inside) dp[pairs] += dp[inside] * dp[pairs - 1 - inside];  // 현재 만들 괄호 쌍 수 순서대로 확인; 첫 괄호 안에 넣을 쌍 수 갱신
//     int answer = (int)dp[n]; free(dp);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // n쌍의 올바른 괄호 문자열 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 모든 올바른 괄호 문자열은 유일하게 (내부 문자열)+뒤쪽 문자열로 나뉨; 내부·뒤쪽의 가능한 쌍 수별 곱을 모두 더하는 카탈란 수 DP
// 예: 2쌍은 (())와 ()() 두 가지, 3쌍은 다섯 가지
// 시간 O(n^2), 공간 O(n).; 이 문제는 나머지 연산 없이 실제 개수를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:38:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_12929_%EC%98%AC%EB%B0%94%EB%A5%B8_%EA%B4%84%ED%98%B8%EC%9D%98_%EA%B0%AF%EC%88%98/README.md)
