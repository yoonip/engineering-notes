# 노란불 신호등

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468371) · Level 1 · C

## 풀이

각 신호등의 주기들의 최소공배수만큼 시각을 확인; 모든 신호등이 노란불인 첫 시각을 반환하고, 한 주기에도 없으면 -1을 반환

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

static long long gcd_value(long long a, long long b) {
    while (b) { long long remainder = a % b; a = b; b = remainder; }
    return a;
}
int solution(int** signals, size_t signals_rows, size_t signals_cols) {
    long long period = 1;
    for (size_t i = 0; i < signals_rows; ++i) {
        long long cycle = signals[i][0] + signals[i][1] + signals[i][2];
        period = period / gcd_value(period, cycle) * cycle;
    }
    for (long long time = 1; time <= period; ++time) {
        bool all_yellow = true;
        for (size_t i = 0; i < signals_rows; ++i) {
            int* signal = signals[i];
            long long pos = (time - 1) % (signal[0] + signal[1] + signal[2]);
            if (pos < signal[0] || pos >= signal[0] + signal[1]) { all_yellow = false; break; }
        }
        if (all_yellow) return (int)time;
    }
    return -1;
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
// static long long gcd_value(long long a, long long b) {  // 나머지를 반복해서 최대공약수 구하기
//     while (b) { long long remainder = a % b; a = b; b = remainder; }  // 나머지가 0이 될 때까지 두 값을 바꿔 최대공약수 계산
//     return a;  // 나머지 연산이 끝난 최대공약수 반환
// }  // 이 범위 끝
// int solution(int** signals, size_t signals_rows, size_t signals_cols) {  // 각 신호등의 주기들의 최소공배수만큼 시각을 확인; 모든 신호등이 노란불인 첫 시각을 반환하고, 한 주기에도 없으면 -1을 반환
//     long long period = 1;  // 모든 신호 패턴의 최소공배수 저장
//     for (size_t i = 0; i < signals_rows; ++i) {  // 확인할 신호등 번호 순서대로 확인
//         long long cycle = signals[i][0] + signals[i][1] + signals[i][2];  // 현재 신호등의 한 주기 저장
//         period = period / gcd_value(period, cycle) * cycle;  // 최대공약수로 먼저 나눈 뒤 곱해 두 주기의 최소공배수를 갱신
//     }  // 이 범위 끝
//     for (long long time = 1; time <= period; ++time) {  // long long 시각을 1부터 전체 반복 주기까지 작은 순서대로 확인
//         bool all_yellow = true;  // 모든 신호가 노란색인지 여부 저장
//         for (size_t i = 0; i < signals_rows; ++i) {  // 확인할 신호등 번호 순서대로 확인
//             int* signal = signals[i];  // 현재 신호등의 초록 노랑 빨강 시간 저장
//             long long pos = (time - 1) % (signal[0] + signal[1] + signal[2]);  // 현재 신호 주기 안의 위치 저장
//             if (pos < signal[0] || pos >= signal[0] + signal[1]) { all_yellow = false; break; }  // 신호 주기에서 노란 구간 밖이면 동시 노란불이 아니므로 중단
//         }  // 이 범위 끝
//         if (all_yellow) return (int)time;  // 모든 신호가 노란색인지 여부가 남아 있으면 확인할 전체 시각로 최종값 계산
//     }  // 이 범위 끝
//     return -1;  // 조건에 맞는 답이 없으면 -1
// }  // 이 범위 끝

// 풀이 요약
// 각 신호등의 주기들의 최소공배수만큼 시각을 확인; 모든 신호등이 노란불인 첫 시각을 반환하고, 한 주기에도 없으면 -1을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:42:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_468371_%EB%85%B8%EB%9E%80%EB%B6%88_%EC%8B%A0%ED%98%B8%EB%93%B1/README.md)
