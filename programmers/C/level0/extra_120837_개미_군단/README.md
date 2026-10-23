# 개미 군단

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120837) · Level 0 · C

## 풀이

공격력 5인 장군개미를 최대한 쓰고, 남은 체력에 3과 1을 순서대로 배치. 몫과 나머지로 필요한 최소 개미 수 계산.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int hp) { return hp / 5 + hp % 5 / 3 + hp % 5 % 3; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int hp) { return hp / 5 + hp % 5 / 3 + hp % 5 % 3; }  // 개미 군단 풀이 시작
// 풀이 요약
// 공격력 5인 장군개미를 최대한 쓰고, 남은 체력에 3과 1을 순서대로 배치. 몫과 나머지로 필요한 최소 개미 수 계산.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:05
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120837_%EA%B0%9C%EB%AF%B8_%EA%B5%B0%EB%8B%A8/README.md)
