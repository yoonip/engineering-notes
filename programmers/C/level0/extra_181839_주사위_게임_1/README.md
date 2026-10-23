# 주사위 게임 1

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181839) · Level 0 · C

## 풀이

둘 다 홀수·하나만 홀수·둘 다 짝수를 순서대로 처리

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int a, int b) {
    if (a % 2 && b % 2) return a * a + b * b;
    if (a % 2 || b % 2) return 2 * (a + b);
    return abs(a - b);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int a, int b) {  // 주사위 게임 1 풀이 시작
//     if (a % 2 && b % 2) return a * a + b * b;  // 두 눈이 모두 홀수이면 제곱의 합 반환
//     if (a % 2 || b % 2) return 2 * (a + b);  // 앞 조건에 해당하지 않고 하나만 홀수이면 두 눈의 합을 두 배로 반환
//     return abs(a - b);  // 둘 다 짝수이면 두 눈 차이의 절댓값 반환
// }  // 블록 끝
// 풀이 요약
// 둘 다 홀수·하나만 홀수·둘 다 짝수를 순서대로 처리
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:24:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181839_%EC%A3%BC%EC%82%AC%EC%9C%84_%EA%B2%8C%EC%9E%84_1/README.md)
