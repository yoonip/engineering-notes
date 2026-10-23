# 종이 자르기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120922) · Level 0 · C

## 풀이

한 조각에서 시작해 한 번 자를 때마다 조각 수가 1 증가. M × N조각까지 늘리는 데 필요한 횟수는 M × N - 1.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int M, int N) { return M * N - 1; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int M, int N) { return M * N - 1; }  // 종이 자르기 풀이 시작
// 풀이 요약
// 한 조각에서 시작해 한 번 자를 때마다 조각 수가 1 증가. M × N조각까지 늘리는 데 필요한 횟수는 M × N - 1.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:24:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120922_%EC%A2%85%EC%9D%B4_%EC%9E%90%EB%A5%B4%EA%B8%B0/README.md)
