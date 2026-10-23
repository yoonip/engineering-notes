# 크기가 작은 부분 문자열

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/147355) · Level 1 · C

## 풀이

p와 같은 길이의 모든 연속 부분 문자열을 비교; 길이가 같으므로 문자별 사전순 비교가 정수 크기 비교와 같음

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

int solution(const char* t, const char* p) {
    size_t n = strlen(t), m = strlen(p); int answer = 0;
    for (size_t i = 0; i + m <= n; ++i) if (strncmp(t + i, p, m) <= 0) ++answer;
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
// int solution(const char* t, const char* p) {  // p와 같은 길이의 모든 연속 부분 문자열을 비교; 길이가 같으므로 문자별 사전순 비교가 정수 크기 비교와 같음
//     size_t n = strlen(t), m = strlen(p); int answer = 0;  // 긴 문자열 t의 길이 / 비교할 p의 길이 / p보다 작거나 같은 부분 수의 개수 저장
//     for (size_t i = 0; i + m <= n; ++i) if (strncmp(t + i, p, m) <= 0) ++answer;  // 잘라 볼 부분 문자열의 시작 순서대로 확인; 찾는 이름 또는 앞부분 문자열이 같으면 p보다 작거나 같은 부분 수의 개수 갱신
//     return answer;  // p보다 작거나 같은 부분 수의 개수 반환
// }  // 이 범위 끝

// 풀이 요약
// p와 같은 길이의 모든 연속 부분 문자열을 비교; 길이가 같으므로 문자별 사전순 비교가 정수 크기 비교와 같음
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:48:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_147355_%ED%81%AC%EA%B8%B0%EA%B0%80_%EC%9E%91%EC%9D%80_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4/README.md)
