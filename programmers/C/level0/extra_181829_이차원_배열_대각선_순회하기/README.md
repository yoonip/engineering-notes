# 이차원 배열 대각선 순회하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181829) · Level 0 · C

## 풀이

모든 행과 열을 순회하면서 행 인덱스와 열 인덱스의 합이 k 이하인 위치만 골라 그 원소를 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int** board, size_t board_rows, size_t board_cols, int k) {
    int sum = 0;
    for (size_t i = 0; i < board_rows; ++i)
        for (size_t j = 0; j < board_cols; ++j) if (i + j <= (size_t)k) sum += board[i][j];
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int** board, size_t board_rows, size_t board_cols, int k) {  // 이차원 배열 대각선 순회하기 풀이 시작
//     int sum = 0;  // 행 번호와 열 번호의 합이 k 이하인 원소를 누적할 sum을 0으로 초기화
//     for (size_t i = 0; i < board_rows; ++i)  // 행 번호 i를 0부터 board_rows - 1까지 순회
//         for (size_t j = 0; j < board_cols; ++j) if (i + j <= (size_t)k) sum += board[i][j];  // 각 열 j를 순회하며 i + j가 k 이하인 칸의 값만 sum에 더하기
//     return sum;  // 지정된 인덱스 합 조건을 만족하는 모든 칸의 합을 반환
// }  // 블록 끝

// 풀이 요약
// 모든 행과 열을 순회하면서 행 인덱스와 열 인덱스의 합이 k 이하인 위치만 골라 그 원소를 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:23:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181829_%EC%9D%B4%EC%B0%A8%EC%9B%90_%EB%B0%B0%EC%97%B4_%EB%8C%80%EA%B0%81%EC%84%A0_%EC%88%9C%ED%9A%8C%ED%95%98%EA%B8%B0/README.md)
