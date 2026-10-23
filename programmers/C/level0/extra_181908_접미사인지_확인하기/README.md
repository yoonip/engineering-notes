# 접미사인지 확인하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181908) · Level 0 · C

## 풀이

후보가 원본보다 길지 않은지 확인하고 끝부분을 비교

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <string.h>

int solution(const char* my_string, const char* is_suffix) {
    size_t n = strlen(my_string), m = strlen(is_suffix);
    return n >= m && strcmp(my_string + n - m, is_suffix) == 0;
}

// 전체 코드 줄별 설명
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// int solution(const char* my_string, const char* is_suffix) {  // 접미사인지 확인하기 풀이 시작
//     size_t n = strlen(my_string), m = strlen(is_suffix);  // strlen으로 원본과 접미사 후보의 길이를 각각 구하기
//     return n >= m && strcmp(my_string + n - m, is_suffix) == 0;  // &&의 단락 평가로 길이를 먼저 확인하고 strcmp로 원본 끝부분과 후보를 비교
// }  // 블록 끝

// 풀이 요약
// 후보가 원본보다 길지 않은지 확인하고 끝부분을 비교
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:08:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181908_%EC%A0%91%EB%AF%B8%EC%82%AC%EC%9D%B8%EC%A7%80_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0/README.md)
