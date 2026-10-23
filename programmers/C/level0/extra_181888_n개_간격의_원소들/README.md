# n개 간격의 원소들

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181888) · Level 0 · C

## 풀이

원본 인덱스 0, n, 2n, …의 원소를 차례로 선택.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int num_list[], size_t num_list_len, int n) {
    size_t length = (num_list_len + n - 1) / n;
    int* answer = malloc(length * sizeof(int));
    for (size_t i = 0; i < length; ++i) answer[i] = num_list[i * n];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int num_list[], size_t num_list_len, int n) {  // n개 간격의 원소들 풀이 시작
//     size_t length = (num_list_len + n - 1) / n;  // 결과의 원소 수 저장
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < length; ++i) answer[i] = num_list[i * n];  // 원본의 0, n, 2n, … 위치를 골라 결과에 순서대로 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 원본 인덱스 0, n, 2n, …의 원소를 차례로 선택.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:06:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181888_n%EA%B0%9C_%EA%B0%84%EA%B2%A9%EC%9D%98_%EC%9B%90%EC%86%8C%EB%93%A4/README.md)
