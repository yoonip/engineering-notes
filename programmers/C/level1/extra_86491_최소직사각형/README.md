# 최소직사각형

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86491) · Level 1 · C

## 풀이

각 명함의 긴 변과 짧은 변을 같은 방향으로 맞추기; 긴 변의 최댓값과 짧은 변의 최댓값을 곱하기

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

int solution(int** sizes, size_t sizes_rows, size_t sizes_cols) {
    int width = 0, height = 0;
    for (size_t i = 0; i < sizes_rows; ++i) {
        int a = sizes[i][0], b = sizes[i][1], longer = a > b ? a : b, shorter = a < b ? a : b;
        if (longer > width) width = longer; if (shorter > height) height = shorter;
    }
    return width * height;
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
// int solution(int** sizes, size_t sizes_rows, size_t sizes_cols) {  // 각 명함의 긴 변과 짧은 변을 같은 방향으로 맞추기; 긴 변의 최댓값과 짧은 변의 최댓값을 곱하기
//     int width = 0, height = 0;  // 각 명함의 긴 변 중 최댓값 / 각 명함의 짧은 변 중 최댓값 저장
//     for (size_t i = 0; i < sizes_rows; ++i) {  // 검사할 명함 위치 순서대로 확인
//         int a = sizes[i][0], b = sizes[i][1], longer = a > b ? a : b, shorter = a < b ? a : b;  // 현재 명함의 첫 변 / 현재 명함의 둘째 변 / 회전 후 긴 변 / 회전 후 짧은 변 저장
//         if (longer > width) width = longer; if (shorter > height) height = shorter;  // 모든 명함을 담도록 긴 변과 짧은 변의 최댓값 갱신
//     }  // 이 범위 끝
//     return width * height;  // 각 명함의 긴 변 중 최댓값 / 각 명함의 짧은 변 중 최댓값로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 각 명함의 긴 변과 짧은 변을 같은 방향으로 맞추기; 긴 변의 최댓값과 짧은 변의 최댓값을 곱하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:52:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_86491_%EC%B5%9C%EC%86%8C%EC%A7%81%EC%82%AC%EA%B0%81%ED%98%95/README.md)
