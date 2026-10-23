# 두 정수 사이의 합

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12912) · Level 1 · C

## 풀이

작은 수부터 큰 수까지의 등차수열 합을 계산; 중간 계산부터 long long을 사용

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

long long solution(int a, int b) {
    long long start = a < b ? a : b, end = a > b ? a : b;
    return (start + end) * (end - start + 1) / 2;
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
// long long solution(int a, int b) {  // 작은 수부터 큰 수까지의 등차수열 합을 계산; 중간 계산부터 long long을 사용
//     long long start = a < b ? a : b, end = a > b ? a : b;  // 두 수 중 작은 끝점 / 두 수 중 큰 끝점 저장
//     return (start + end) * (end - start + 1) / 2;  // 두 수 중 작은 끝점 / 두 수 중 큰 끝점로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 작은 수부터 큰 수까지의 등차수열 합을 계산; 중간 계산부터 long long을 사용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12912_%EB%91%90_%EC%A0%95%EC%88%98_%EC%82%AC%EC%9D%B4%EC%9D%98_%ED%95%A9/README.md)
