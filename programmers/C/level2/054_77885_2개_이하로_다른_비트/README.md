# 2개 이하로 다른 비트

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77885) · Level 2 · C

## 풀이

짝수는 마지막 0을 1로 바꾸면 됨; 홀수는 오른쪽 첫 0을 1로, 바로 아래 1을 0으로 바꾸면 가장 작은 증가량

예: 7(111)→11(1011), 바뀐 비트는 두 개; 제한 내 정수 연산 기준 시간·결과 공간 O(N)

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

long long* solution(long long numbers[], size_t numbers_len) {
    long long* answer = malloc(numbers_len * sizeof(*answer));
    for (size_t i = 0; i < numbers_len; ++i) {
        unsigned long long value = (unsigned long long)numbers[i];
        unsigned long long zero = (~value) & (value + 1);
        answer[i] = (long long)(value + zero - (zero >> 1));
    }
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
// long long* solution(long long numbers[], size_t numbers_len) {  // 짝수는 마지막 0을 1로 바꾸면 됨; 홀수는 오른쪽 첫 0을 1로, 바로 아래 1을 0으로 바꾸면 가장 작은 증가량
//     long long* answer = malloc(numbers_len * sizeof(*answer));  // 각 수보다 크고 두 비트 이하로 다른 수 공간 확보
//     for (size_t i = 0; i < numbers_len; ++i) {  // 변환할 수 위치 순서대로 확인
//         unsigned long long value = (unsigned long long)numbers[i];  // 현재 입력을 부호 없는 정수로 바꾼 값 저장
//         unsigned long long zero = (~value) & (value + 1);  // 오른쪽에서 처음 나온 0 비트 저장
//         answer[i] = (long long)(value + zero - (zero >> 1));  // 각 수보다 크고 두 비트 이하로 다른 수 갱신
//     }  // 이 범위 끝
//     return answer;  // 각 수보다 크고 두 비트 이하로 다른 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 짝수는 마지막 0을 1로 바꾸면 됨; 홀수는 오른쪽 첫 0을 1로, 바로 아래 1을 0으로 바꾸면 가장 작은 증가량
// 예: 7(111)→11(1011), 바뀐 비트는 두 개; 제한 내 정수 연산 기준 시간·결과 공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/054_77885_2%EA%B0%9C_%EC%9D%B4%ED%95%98%EB%A1%9C_%EB%8B%A4%EB%A5%B8_%EB%B9%84%ED%8A%B8/README.md)
