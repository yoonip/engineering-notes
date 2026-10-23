# 명예의 전당 (1)

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/138477) · Level 1 · C

## 풀이

매일까지의 상위 k개 점수를 유지하고 그중 최솟값을 기록; C는 정렬된 배열을, C++는 최소 힙을 사용

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

int* solution(int k, int score[], size_t score_len) {
    int* hall = malloc(k * sizeof(int)); size_t length = 0;
    int* answer = malloc(score_len * sizeof(int));
    for (size_t i = 0; i < score_len; ++i) {
        if (length < (size_t)k) hall[length++] = score[i]; else if (score[i] > hall[0]) hall[0] = score[i];
        for (size_t j = 1; j < length; ++j) { int value = hall[j]; size_t p = j; while (p && hall[p - 1] > value) { hall[p] = hall[p - 1]; --p; } hall[p] = value; }
        answer[i] = hall[0];
    }
    free(hall);
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
// int* solution(int k, int score[], size_t score_len) {  // 매일까지의 상위 k개 점수를 유지하고 그중 최솟값을 기록; C는 정렬된 배열을, C++는 최소 힙을 사용
//     int* hall = malloc(k * sizeof(int)); size_t length = 0;  // 오름차순 명예의 전당 점수 / 현재 전당에 들어간 점수 수 공간 확보
//     int* answer = malloc(score_len * sizeof(int));  // 날짜별 전당 최저 점수 공간 확보
//     for (size_t i = 0; i < score_len; ++i) {  // 오늘 점수 위치 순서대로 확인
//         if (length < (size_t)k) hall[length++] = score[i]; else if (score[i] > hall[0]) hall[0] = score[i];  // 전당이 덜 찼으면 추가하고 꽉 찼으면 현재 최하위보다 높은 점수만 교체
//         for (size_t j = 1; j < length; ++j) { int value = hall[j]; size_t p = j; while (p && hall[p - 1] > value) { hall[p] = hall[p - 1]; --p; } hall[p] = value; }  // 삽입 정렬할 위치 순서대로 확인; 제자리를 찾는 점수 / 앞 점수와 비교할 위치 / 오름차순 명예의 전당 점수 저장
//         answer[i] = hall[0];  // 날짜별 전당 최저 점수 갱신
//     }  // 이 범위 끝
//     free(hall);  // 오름차순 명예의 전당 점수 임시 공간 정리
//     return answer;  // 날짜별 전당 최저 점수 반환
// }  // 이 범위 끝

// 풀이 요약
// 매일까지의 상위 k개 점수를 유지하고 그중 최솟값을 기록; C는 정렬된 배열을, C++는 최소 힙을 사용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:49:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_138477_%EB%AA%85%EC%98%88%EC%9D%98_%EC%A0%84%EB%8B%B9_%281%29/README.md)
