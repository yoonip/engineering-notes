# 바탕화면 정리

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/161990) · Level 1 · C

## 풀이

파일이 있는 칸의 최소 행·열과 최대 행·열을 계산; 오른쪽 아래 경계는 파일 칸보다 한 칸 뒤로 정하기

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

int* solution(const char* wallpaper[], size_t wallpaper_len) {
    int top = (int)wallpaper_len, left = (int)strlen(wallpaper[0]), bottom = 0, right = 0;
    for (size_t r = 0; r < wallpaper_len; ++r) for (size_t c = 0; wallpaper[r][c]; ++c) if (wallpaper[r][c] == '#') {
        if ((int)r < top) top = (int)r; if ((int)c < left) left = (int)c;
        if ((int)r + 1 > bottom) bottom = (int)r + 1; if ((int)c + 1 > right) right = (int)c + 1;
    }
    int* answer = malloc(4 * sizeof(int)); answer[0] = top; answer[1] = left; answer[2] = bottom; answer[3] = right;
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
// int* solution(const char* wallpaper[], size_t wallpaper_len) {  // 파일이 있는 칸의 최소 행·열과 최대 행·열을 계산; 오른쪽 아래 경계는 파일 칸보다 한 칸 뒤로 정하기
//     int top = (int)wallpaper_len, left = (int)strlen(wallpaper[0]), bottom = 0, right = 0;  // 파일이 있는 최소 행 / 파일이 있는 최소 열 / 파일을 포함하는 아래 경계 / 파일을 포함하는 오른쪽 경계 저장
//     for (size_t r = 0; r < wallpaper_len; ++r) for (size_t c = 0; wallpaper[r][c]; ++c) if (wallpaper[r][c] == '#') {  // 파일을 찾을 행 순서대로 확인; 파일을 찾을 열 갱신
//         if ((int)r < top) top = (int)r; if ((int)c < left) left = (int)c;  // 파일이 있는 행과 열의 최솟값 갱신
//         if ((int)r + 1 > bottom) bottom = (int)r + 1; if ((int)c + 1 > right) right = (int)c + 1;  // 파일 칸을 포함하도록 행·열에 1을 더해 드래그 아래·오른쪽 경계 갱신
//     }  // 이 범위 끝
//     int* answer = malloc(4 * sizeof(int)); answer[0] = top; answer[1] = left; answer[2] = bottom; answer[3] = right;  // 모든 파일을 감싸는 드래그 범위 공간 확보
//     return answer;  // 모든 파일을 감싸는 드래그 범위 반환
// }  // 이 범위 끝

// 풀이 요약
// 파일이 있는 칸의 최소 행·열과 최대 행·열을 계산; 오른쪽 아래 경계는 파일 칸보다 한 칸 뒤로 정하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:46:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_161990_%EB%B0%94%ED%83%95%ED%99%94%EB%A9%B4_%EC%A0%95%EB%A6%AC/README.md)
