# 홀짝 구분하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181944) · Level 0 · C

## 풀이

2로 나눈 나머지에 따라 짝수와 홀수 출력 형식을 선택

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    printf("%d is %s\n", n, n % 2 == 0 ? "even" : "odd");
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int n;  // 짝홀을 판단할 입력 정수 n 준비
//     if (scanf("%d", &n) != 1) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     printf("%d is %s\n", n, n % 2 == 0 ? "even" : "odd");  // printf의 형식 지정자와 이스케이프 문자로 요구된 형식의 결과를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝
// 풀이 요약
// 2로 나눈 나머지에 따라 짝수와 홀수 출력 형식을 선택
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:26:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181944_%ED%99%80%EC%A7%9D_%EA%B5%AC%EB%B6%84%ED%95%98%EA%B8%B0/README.md)
