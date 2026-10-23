# 간단한 식 계산하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181865) · Level 0 · C

## 풀이

문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* binomial) {
    int a, b;
    char op;
    sscanf(binomial, "%d %c %d", &a, &op, &b);
    return op == '+' ? a + b : op == '-' ? a - b : a * b;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* binomial) {  // 간단한 식 계산하기 풀이 시작
//     int a, b;  // 식의 왼쪽·오른쪽 정수 a와 b 준비
//     char op;  // 적용할 연산자 한 글자 저장
//     sscanf(binomial, "%d %c %d", &a, &op, &b);  // sscanf의 %d·%c 형식으로 피연산자와 연산자를 읽기
//     return op == '+' ? a + b : op == '-' ? a - b : a * b;  // 연산자가 +면 합, -면 차, 그 외 *면 곱 반환
// }  // 블록 끝
// 풀이 요약
// 문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:17:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181865_%EA%B0%84%EB%8B%A8%ED%95%9C_%EC%8B%9D_%EA%B3%84%EC%82%B0%ED%95%98%EA%B8%B0/README.md)
