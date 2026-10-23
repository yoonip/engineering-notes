# 할인 행사

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131127) · Level 2 · C

## 풀이

연속한 열흘마다 할인 상품 개수를 세어 원하는 상품별 수량과 비교; 필요한 수량 합이 10이라 정확히 일치해야 하기
예: 첫 예제는 3·4·5일 시작이 가능해 3.; 할인 날짜 D개일 때 시간 O(10D), 구간 집계 공간 O(10)

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

int solution(const char* want[], size_t want_len, int number[], size_t number_len, const char* discount[], size_t discount_len) {
    (void)number_len;
    int* count = calloc(want_len, sizeof(*count)); int answer = 0;
    for (size_t i = 0; i < discount_len; ++i) {
        for (size_t j = 0; j < want_len; ++j) {
            if (!strcmp(discount[i], want[j])) ++count[j];
            if (i >= 10 && !strcmp(discount[i - 10], want[j])) --count[j];
        }
        if (i >= 9) {
            bool valid = true;
            for (size_t j = 0; j < want_len; ++j) if (count[j] != number[j]) valid = false;
            answer += valid;
        }
    }
    free(count);
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
// int solution(const char* want[], size_t want_len, int number[], size_t number_len, const char* discount[], size_t discount_len) {  // 연속한 열흘마다 할인 상품 개수를 세어 원하는 상품별 수량과 비교; 필요한 수량 합이 10이라 정확히 일치해야 하기
//     (void)number_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* count = calloc(want_len, sizeof(*count)); int answer = 0;  // 최근 열흘의 원하는 품목별 개수 / 조건에 맞는 가입 시작일 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < discount_len; ++i) {  // 할인 일정의 현재 날짜 순서대로 확인
//         for (size_t j = 0; j < want_len; ++j) {  // 원하는 품목 번호 순서대로 확인
//             if (!strcmp(discount[i], want[j])) ++count[j];  // 찾는 이름 또는 앞부분 문자열이 같으면 최근 열흘의 원하는 품목별 개수 갱신
//             if (i >= 10 && !strcmp(discount[i - 10], want[j])) --count[j];  // 찾는 이름 또는 앞부분 문자열이 같으면 최근 열흘의 원하는 품목별 개수 갱신
//         }  // 이 범위 끝
//         if (i >= 9) {  // 할인 일정의 현재 날짜가 9 이상이면 처리
//             bool valid = true;  // 최근 열흘과 필요 개수가 같은지 여부 저장
//             for (size_t j = 0; j < want_len; ++j) if (count[j] != number[j]) valid = false;  // 원하는 품목 중 개수가 하나라도 다르면 이 시작일은 제외
//             answer += valid;  // 조건에 맞는 가입 시작일 수 / 최근 열흘과 필요 개수가 같은지 여부 더해 누적
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(count);  // 최근 열흘의 원하는 품목별 개수 임시 공간 정리
//     return answer;  // 조건에 맞는 가입 시작일 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 연속한 열흘마다 할인 상품 개수를 세어 원하는 상품별 수량과 비교; 필요한 수량 합이 10이라 정확히 일치해야 하기
// 예: 첫 예제는 3·4·5일 시작이 가능해 3.; 할인 날짜 D개일 때 시간 O(10D), 구간 집계 공간 O(10)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/042_131127_%ED%95%A0%EC%9D%B8_%ED%96%89%EC%82%AC/README.md)
