# 짝수와 홀수

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12937) · Level 1 · C

## 풀이

2로 나눈 나머지가 0이면 Even, 아니면 Odd를 반환

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
char* solution(int num) { return copy_text(num % 2 == 0 ? "Even" : "Odd"); }

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
//     char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;  // Even 또는 Odd 문자열 사본 공간 확보
// }  // 이 범위 끝
// char* solution(int num) { return copy_text(num % 2 == 0 ? "Even" : "Odd"); }  // 2로 나눈 나머지가 0이면 Even, 아니면 Odd를 반환

// 풀이 요약
// 2로 나눈 나머지가 0이면 Even, 아니면 Odd를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:56:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_12937_%EC%A7%9D%EC%88%98%EC%99%80_%ED%99%80%EC%88%98/README.md)
