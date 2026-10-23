# 두 수의 나눗셈

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120806) · Level 0 · C

## 풀이

num1에 1000을 먼저 곱하고 num2로 정수 나눗셈. 실수 연산 없이 두 수의 비에 1000을 곱한 값의 정수 부분 계산.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int num1, int num2) { return num1 * 1000 / num2; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int num1, int num2) { return num1 * 1000 / num2; }  // 두 수의 나눗셈 풀이 시작
// 풀이 요약
// num1에 1000을 먼저 곱하고 num2로 정수 나눗셈. 실수 연산 없이 두 수의 비에 1000을 곱한 값의 정수 부분 계산.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:54:54
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120806_%EB%91%90_%EC%88%98%EC%9D%98_%EB%82%98%EB%88%97%EC%85%88/README.md)
