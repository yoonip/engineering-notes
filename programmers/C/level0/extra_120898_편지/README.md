# 편지

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120898) · Level 0 · C

## 풀이

공백도 한 글자로 세어 전체 문자열 길이에 2를 곱하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* message) { return 2 * (int)strlen(message); }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* message) { return 2 * (int)strlen(message); }  // 편지 풀이 시작

// 풀이 요약
// 공백도 한 글자로 세어 전체 문자열 길이에 2를 곱하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120898_%ED%8E%B8%EC%A7%80/README.md)
