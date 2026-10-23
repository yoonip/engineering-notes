# 부분 문자열

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181842) · Level 0 · C

## 풀이

포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* str1, const char* str2) { return strstr(str2, str1) != NULL; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* str1, const char* str2) { return strstr(str2, str1) != NULL; }  // 부분 문자열 풀이 시작

// 풀이 요약
// 포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:23:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181842_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4/README.md)
