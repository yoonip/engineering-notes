# a와 b 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181951) · Level 0 · C

## 풀이

입력받은 두 정수를 변수 이름과 함께 각각 출력

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    int a, b;
    if (scanf("%d %d", &a, &b) != 2) return 0;
    printf("a = %d\nb = %d\n", a, b);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 두 입력 정수를 담을 int형 변수를 선언
//     if (scanf("%d %d", &a, &b) != 2) return 0;  // &로 변수 주소를 전달해 정수를 읽고 입력 개수를 확인
//     printf("a = %d\nb = %d\n", a, b);  // %d에 정수를 넣고 \n으로 줄을 바꿔 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 두 정수를 변수 이름과 함께 각각 출력
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:25:54
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181951_a%EC%99%80_b_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
