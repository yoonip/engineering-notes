# 피자 나눠 먹기 (1)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120814) · Level 0 · C

## 풀이

사람마다 한 조각 이상 받으려면 사람 수를 7로 나눈 값을 올림한 만큼의 피자가 필요

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) { return (n + 6) / 7; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) { return (n + 6) / 7; }  // 피자 나눠 먹기 (1) 풀이 시작

// 풀이 요약
// 사람마다 한 조각 이상 받으려면 사람 수를 7로 나눈 값을 올림한 만큼의 피자가 필요
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:34:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120814_%ED%94%BC%EC%9E%90_%EB%82%98%EB%88%A0_%EB%A8%B9%EA%B8%B0_%281%29/README.md)
