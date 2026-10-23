# 과일 장수

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/135808) · Level 1 · C

## 풀이

점수를 내림차순으로 정렬해 m개씩 묶기; 각 묶음의 최솟값에 m을 곱해 합산하고 남는 과일은 제외하기

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

static int descending_int(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b; return (y > x) - (y < x);
}
int solution(int k, int m, int score[], size_t score_len) {
    int* sorted = malloc(score_len * sizeof(int)); memcpy(sorted, score, score_len * sizeof(int)); qsort(sorted, score_len, sizeof(int), descending_int);
    int answer = 0;
    for (size_t i = m - 1; i < score_len; i += m) answer += sorted[i] * m;
    free(sorted);
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
// static int descending_int(const void* a, const void* b) {  // 큰 점수부터 정렬
//     int x = *(const int*)a, y = *(const int*)b; return (y > x) - (y < x);  // 비교할 첫 점수 / 비교할 둘째 점수 저장
// }  // 이 범위 끝
// int solution(int k, int m, int score[], size_t score_len) {  // 점수를 내림차순으로 정렬해 m개씩 묶기; 각 묶음의 최솟값에 m을 곱해 합산하고 남는 과일은 제외하기
//     int* sorted = malloc(score_len * sizeof(int)); memcpy(sorted, score, score_len * sizeof(int)); qsort(sorted, score_len, sizeof(int), descending_int);  // 점수 내림차순 사본 공간 확보
//     int answer = 0;  // 팔 수 있는 상자의 총금액 저장
//     for (size_t i = m - 1; i < score_len; i += m) answer += sorted[i] * m;  // 각 상자의 최저 점수 위치 순서대로 확인; 팔 수 있는 상자의 총금액 / 점수 내림차순 사본 / 각 상자의 최저 점수 위치 더해 누적
//     free(sorted);  // 점수 내림차순 사본 임시 공간 정리
//     return answer;  // 팔 수 있는 상자의 총금액 반환
// }  // 이 범위 끝

// 풀이 요약
// 점수를 내림차순으로 정렬해 m개씩 묶기; 각 묶음의 최솟값에 m을 곱해 합산하고 남는 과일은 제외하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:50:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_135808_%EA%B3%BC%EC%9D%BC_%EC%9E%A5%EC%88%98/README.md)
