# 배열의 길이를 2의 거듭제곱으로 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181857) · Level 0 · C

## 풀이

1부터 두 배씩 늘려 원래 배열 길이 이상인 가장 작은 2의 거듭제곱을 찾기. 해당 길이의 배열을 0으로 초기화한 뒤 원래 원소만 앞부분에 복사

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    size_t length = 1;
    while (length < arr_len) length *= 2;
    int* answer = calloc(length, sizeof(int));
    memcpy(answer, arr, arr_len * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 배열의 길이를 2의 거듭제곱으로 만들기 풀이 시작
//     size_t length = 1;  // 반환 배열의 길이 후보 length를 가장 작은 2의 거듭제곱인 1로 초기화
//     while (length < arr_len) length *= 2;  // length가 원래 길이보다 작을 동안 두 배로 늘려 필요한 최소 길이를 찾기
//     int* answer = calloc(length, sizeof(int));  // calloc으로 length개의 int 공간을 할당하고 모든 원소를 0으로 초기화
//     memcpy(answer, arr, arr_len * sizeof(int));  // memcpy로 원래 원소 arr_len개를 앞부분에 복사하여 추가된 뒷부분의 0을 유지
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 1부터 두 배씩 늘려 원래 배열 길이 이상인 가장 작은 2의 거듭제곱을 찾기. 해당 길이의 배열을 0으로 초기화한 뒤 원래 원소만 앞부분에 복사
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:17:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181857_%EB%B0%B0%EC%97%B4%EC%9D%98_%EA%B8%B8%EC%9D%B4%EB%A5%BC_2%EC%9D%98_%EA%B1%B0%EB%93%AD%EC%A0%9C%EA%B3%B1%EC%9C%BC%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
