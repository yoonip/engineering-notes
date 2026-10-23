# 문자열 붙여서 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181946) · Level 0 · C

## 풀이

공백으로 구분한 두 문자열을 붙여 출력

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    char first[100001], second[100001];
    if (scanf("%100000s %100000s", first, second) != 2) return 0;
    printf("%s%s\n", first, second);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char first[100001], second[100001];  // 입력 문자열 두 개를 각각 저장할 char형 배열을 선언
//     if (scanf("%100000s %100000s", first, second) != 2) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     printf("%s%s\n", first, second);  // printf의 형식 지정자와 이스케이프 문자로 요구된 형식의 결과를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 공백으로 구분한 두 문자열을 붙여 출력
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:26:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181946_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%B6%99%EC%97%AC%EC%84%9C_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
