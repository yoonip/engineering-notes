# 수열과 구간 쿼리 1

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181883) · Level 0 · C

## 풀이

각 닫힌 구간에 속한 원소를 모두 1씩 증가

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {
    int* answer = malloc(arr_len * sizeof(int));
    memcpy(answer, arr, arr_len * sizeof(int));
    for (size_t q = 0; q < queries_rows; ++q)
        for (int i = queries[q][0]; i <= queries[q][1]; ++i) ++answer[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {  // 수열과 구간 쿼리 1 풀이 시작
//     int* answer = malloc(arr_len * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, arr, arr_len * sizeof(int));  // memcpy로 지정한 바이트 수만큼 원소를 목적지에 복사
//     for (size_t q = 0; q < queries_rows; ++q)  // 입력 순서대로 각 구간 증가 쿼리 적용
//         for (int i = queries[q][0]; i <= queries[q][1]; ++i) ++answer[i];  // 쿼리의 시작·끝 인덱스를 포함해 구간의 모든 값에 1 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 닫힌 구간에 속한 원소를 모두 1씩 증가
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:13:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181883_%EC%88%98%EC%97%B4%EA%B3%BC_%EA%B5%AC%EA%B0%84_%EC%BF%BC%EB%A6%AC_1/README.md)
