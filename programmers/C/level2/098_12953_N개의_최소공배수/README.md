# N개의 최소공배수

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12953) · Level 2 · C

## 풀이

현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산; 두 수의 곱에서 공통 인수인 최대공약수를 한 번 나누기
예: [2,6,8,14]는 2→6→24→168.; 정수 연산 기준 N개·중간 최대값 V에 대해 시간 O(N log V), 공간 O(1)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int gcd(int a, int b) {
    while (b) { int r = a % b; a = b; b = r; }
    return a;
}
int solution(int arr[], size_t arr_len) {
    int answer = 1;
    for (size_t i = 0; i < arr_len; ++i) answer = answer / gcd(answer, arr[i]) * arr[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static int gcd(int a, int b) {  // 나머지를 반복해서 최대공약수 구하기
//     while (b) { int r = a % b; a = b; b = r; }  // 나머지가 0이 될 때까지 두 값을 바꿔 최대공약수 계산
//     return a;  // 나머지가 0이 된 시점의 최대공약수 반환
// }  // 이 범위 끝
// int solution(int arr[], size_t arr_len) {  // 현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산; 두 수의 곱에서 공통 인수인 최대공약수를 한 번 나누기
//     int answer = 1;  // 지금까지 원소들의 최소공배수 저장
//     for (size_t i = 0; i < arr_len; ++i) answer = answer / gcd(answer, arr[i]) * arr[i];  // 최소공배수에 합칠 원소 위치 순서대로 확인; 지금까지 원소들의 최소공배수 갱신
//     return answer;  // 지금까지 원소들의 최소공배수 반환
// }  // 이 범위 끝

// 풀이 요약
// 현재까지의 최소공배수와 다음 수의 최소공배수를 반복 계산; 두 수의 곱에서 공통 인수인 최대공약수를 한 번 나누기
// 예: [2,6,8,14]는 2→6→24→168.; 정수 연산 기준 N개·중간 최대값 V에 대해 시간 O(N log V), 공간 O(1)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/098_12953_N%EA%B0%9C%EC%9D%98_%EC%B5%9C%EC%86%8C%EA%B3%B5%EB%B0%B0%EC%88%98/README.md)
