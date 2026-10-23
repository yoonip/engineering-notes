# 2016년

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12901) · Level 1 · C

## 풀이

윤년인 2016년의 월별 일수를 누적하고 1월 1일 금요일을 기준으로 요일을 계산

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
char* solution(int a, int b) {
    int days[12] = {31,29,31,30,31,30,31,31,30,31,30,31}; const char* weekdays[7] = {"FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"};
    int elapsed = b - 1; for (int month = 0; month < a - 1; ++month) elapsed += days[month];
    return copy_text(weekdays[elapsed % 7]);
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
//     char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;  // 요일 문자열 사본 공간 확보
// }  // 이 범위 끝
// char* solution(int a, int b) {  // 윤년인 2016년의 월별 일수를 누적하고 1월 1일 금요일을 기준으로 요일을 계산
//     int days[12] = {31,29,31,30,31,30,31,31,30,31,30,31}; const char* weekdays[7] = {"FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"};  // 윤년의 월별 일수 / 금요일부터 시작하는 요일표 저장
//     int elapsed = b - 1; for (int month = 0; month < a - 1; ++month) elapsed += days[month];  // 1월 1일부터 지난 날짜 수 / 날짜에 더할 이전 달 저장
//     return copy_text(weekdays[elapsed % 7]);  // 금요일부터 시작하는 요일표 / 1월 1일부터 지난 날짜 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 윤년인 2016년의 월별 일수를 누적하고 1월 1일 금요일을 기준으로 요일을 계산
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:43
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12901_2016%EB%85%84/README.md)
