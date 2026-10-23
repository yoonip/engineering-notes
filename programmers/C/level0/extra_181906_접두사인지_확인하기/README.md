# 접두사인지 확인하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181906) · Level 0 · C

## 풀이

원본의 시작 부분과 접두사 후보를 비교

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <string.h>

int solution(const char* my_string, const char* is_prefix) {
    return strncmp(my_string, is_prefix, strlen(is_prefix)) == 0;
}

// 전체 코드 줄별 설명
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// int solution(const char* my_string, const char* is_prefix) {  // 접두사인지 확인하기 풀이 시작
//     return strncmp(my_string, is_prefix, strlen(is_prefix)) == 0;  // strncmp로 접두사 후보 길이만큼 비교하고 결과가 0인지 반환
// }  // 블록 끝

// 풀이 요약
// 원본의 시작 부분과 접두사 후보를 비교
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:09:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181906_%EC%A0%91%EB%91%90%EC%82%AC%EC%9D%B8%EC%A7%80_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0/README.md)
