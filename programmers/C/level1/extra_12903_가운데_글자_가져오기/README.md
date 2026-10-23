# 가운데 글자 가져오기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12903) · Level 1 · C

## 풀이

길이가 홀수이면 가운데 한 글자, 짝수이면 가운데 두 글자를 자르기

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

char* solution(const char* s) {
    size_t n = strlen(s), length = n % 2 ? 1 : 2;
    char* answer = malloc(length + 1); memcpy(answer, s + (n - 1) / 2, length); answer[length] = '\0';
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
// char* solution(const char* s) {  // 길이가 홀수이면 가운데 한 글자, 짝수이면 가운데 두 글자를 자르기
//     size_t n = strlen(s), length = n % 2 ? 1 : 2;  // 입력 문자열 길이 / 가운데에서 가져올 글자 수 저장
//     char* answer = malloc(length + 1); memcpy(answer, s + (n - 1) / 2, length); answer[length] = '\0';  // 가운데 한 글자 또는 두 글자 공간 확보
//     return answer;  // 가운데 한 글자 또는 두 글자 반환
// }  // 이 범위 끝

// 풀이 요약
// 길이가 홀수이면 가운데 한 글자, 짝수이면 가운데 두 글자를 자르기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_12903_%EA%B0%80%EC%9A%B4%EB%8D%B0_%EA%B8%80%EC%9E%90_%EA%B0%80%EC%A0%B8%EC%98%A4%EA%B8%B0/README.md)
