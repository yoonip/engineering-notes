# 직각삼각형 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120823) · Level 0 · C

## 풀이

첫 행부터 별을 1개,2개 순서로 늘려 n개까지 출력

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 1; i <= n; ++i) {
        for (int j = 0; j < i; ++j) putchar('*');
        putchar('\n');
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int n;  // 삼각형의 마지막 행 별 수이자 전체 행 수 n 준비
//     if (scanf("%d", &n) != 1) return 0;  // scanf로 표준 입력의 정수를 읽으며, 읽기에 실패하면 프로그램을 종료
//     for (int i = 1; i <= n; ++i) {  // 현재 행의 별 수 i를 1부터 n까지 증가
//         for (int j = 0; j < i; ++j) putchar('*');  // 현재 행에 별 i개 출력
//         putchar('\n');  // 한 행의 별을 출력한 뒤 줄바꿈
//     }  // 블록 끝
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝
// 풀이 요약
// 첫 행부터 별을 1개,2개 순서로 늘려 n개까지 출력
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120823_%EC%A7%81%EA%B0%81%EC%82%BC%EA%B0%81%ED%98%95_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
