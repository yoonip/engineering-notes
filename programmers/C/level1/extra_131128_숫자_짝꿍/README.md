# 숫자 짝꿍

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131128) · Level 1 · C

## 풀이

두 문자열에서 각 숫자의 등장 횟수를 세기; 공통 개수만큼 큰 숫자부터 붙이고 공통 숫자가 없거나 0만 있는 경우를 따로 처리

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

static char* copy_text(const char* text) {
    char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;
}
char* solution(const char* X, const char* Y) {
    int x[10] = {0}, y[10] = {0};
    for (size_t i = 0; X[i]; ++i) ++x[X[i] - '0']; for (size_t i = 0; Y[i]; ++i) ++y[Y[i] - '0'];
    size_t length = 0; for (int digit = 0; digit < 10; ++digit) length += x[digit] < y[digit] ? x[digit] : y[digit];
    if (!length) return copy_text("-1");
    char* answer = malloc(length + 1); size_t out = 0;
    for (int digit = 9; digit >= 0; --digit) { int count = x[digit] < y[digit] ? x[digit] : y[digit]; for (int j = 0; j < count; ++j) answer[out++] = '0' + digit; }
    answer[out] = '\0';
    if (answer[0] == '0') answer[1] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// static char* copy_text(const char* text) {  // 문자열을 새 공간에 복사해서 돌려주기
//     char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;  // 문자열 길이와 널 문자 공간을 확보해서 원문 사본 반환
// }  // 이 범위 끝
// char* solution(const char* X, const char* Y) {  // 두 문자열에서 각 숫자의 등장 횟수를 세기; 공통 개수만큼 큰 숫자부터 붙이고 공통 숫자가 없거나 0만 있는 경우를 따로 처리
//     int x[10] = {0}, y[10] = {0};  // X의 숫자별 등장 횟수 / Y의 숫자별 등장 횟수 저장
//     for (size_t i = 0; X[i]; ++i) ++x[X[i] - '0']; for (size_t i = 0; Y[i]; ++i) ++y[Y[i] - '0'];  // X와 Y에서 숫자별 등장 횟수 따로 세기
//     size_t length = 0; for (int digit = 0; digit < 10; ++digit) length += x[digit] < y[digit] ? x[digit] : y[digit];  // 공통으로 쓸 수 있는 자릿수 / 꺼낼 공통 숫자 저장
//     if (!length) return copy_text("-1");  // 공통으로 쓸 숫자가 없으면 -1 문자열 반환
//     char* answer = malloc(length + 1); size_t out = 0;  // 공통 숫자로 만든 가장 큰 수 / 큰 숫자부터 채울 위치 공간 확보
//     for (int digit = 9; digit >= 0; --digit) { int count = x[digit] < y[digit] ? x[digit] : y[digit]; for (int j = 0; j < count; ++j) answer[out++] = '0' + digit; }  // 꺼낼 공통 숫자 순서대로 확인; 현재 숫자를 함께 쓸 횟수 / 공통 숫자로 만든 가장 큰 수 저장
//     answer[out] = '\0';  // 문자열 끝에 널 문자 붙이기
//     if (answer[0] == '0') answer[1] = '\0';  // 가장 앞 숫자가 0이면 모두 0뿐이므로 결과를 한 글자 0으로 줄이기
//     return answer;  // 공통 숫자로 만든 가장 큰 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 문자열에서 각 숫자의 등장 횟수를 세기; 공통 개수만큼 큰 숫자부터 붙이고 공통 숫자가 없거나 0만 있는 경우를 따로 처리
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:51:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_131128_%EC%88%AB%EC%9E%90_%EC%A7%9D%EA%BF%8D/README.md)
