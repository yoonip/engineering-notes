# 덧셈식 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181947) · Level 0 · C

## 풀이

덧셈을 계산하고 요구된 공백과 기호를 포함해 출력

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    printf("%d + %d = %d\n", a, b, a + b);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 입력 정수 두 개를 저장할 int형 변수를 선언
//     if (scanf("%d %d", &a, &b) != 2) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     printf("%d + %d = %d\n", a, b, a + b);  // printf의 형식 지정자와 이스케이프 문자로 요구된 형식의 결과를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 덧셈을 계산하고 요구된 공백과 기호를 포함해 출력
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:26:11
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181947_%EB%8D%A7%EC%85%88%EC%8B%9D_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
