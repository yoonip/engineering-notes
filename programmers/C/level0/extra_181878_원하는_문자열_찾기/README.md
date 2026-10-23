# 원하는 문자열 찾기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181878) · Level 0 · C

## 풀이

양쪽 문자열을 모두 소문자로 바꿔 대소문자를 구분하지 않고 찾기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* myString, const char* pat) {
    size_t n = strlen(myString), m = strlen(pat);
    if (m > n) return 0;
    for (size_t i = 0; i + m <= n; ++i) {
        size_t j = 0;
        while (j < m && tolower((unsigned char)myString[i + j]) == tolower((unsigned char)pat[j])) ++j;
        if (j == m) return 1;
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* myString, const char* pat) {  // 원하는 문자열 찾기 풀이 시작
//     size_t n = strlen(myString), m = strlen(pat);  // 원본 길이 n과 찾을 패턴 길이 m 저장
//     if (m > n) return 0;  // 패턴이 원본보다 길면 포함될 수 없으므로 0 반환
//     for (size_t i = 0; i + m <= n; ++i) {  // 패턴 길이만큼 비교할 수 있는 모든 시작 위치 검사
//         size_t j = 0;  // 이번 시작점에서 일치한 패턴 문자 수를 0으로 시작
//         while (j < m && tolower((unsigned char)myString[i + j]) == tolower((unsigned char)pat[j])) ++j;  // 대소문자를 구분하지 않도록 양쪽 문자를 소문자로 바꿔 연속 일치 길이 증가
//         if (j == m) return 1;  // 패턴 전체가 일치한 시작점을 찾으면 1 반환
//     }  // 블록 끝
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝
// 풀이 요약
// 양쪽 문자열을 모두 소문자로 바꿔 대소문자를 구분하지 않고 찾기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:14:45
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181878_%EC%9B%90%ED%95%98%EB%8A%94_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%B0%BE%EA%B8%B0/README.md)
