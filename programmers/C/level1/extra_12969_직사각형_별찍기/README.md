# 직사각형 별찍기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12969) · Level 1 · C

## 풀이

가로 n개의 별을 출력하고 줄을 바꾸는 작업을 세로 m번 반복하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int main(void) {
    int n, m; if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int row = 0; row < m; ++row) { for (int col = 0; col < n; ++col) putchar('*'); putchar('\n'); }
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int main(void) {  // 가로 n개의 별을 출력하고 줄을 바꾸는 작업을 세로 m번 반복하기
//     int n, m; if (scanf("%d %d", &n, &m) != 2) return 0;  // 별 출력을 정상적으로 마치고 프로그램 종료
//     for (int row = 0; row < m; ++row) { for (int col = 0; col < n; ++col) putchar('*'); putchar('\n'); }  // 출력 중인 행 순서대로 확인; 별을 한 줄 채우고 줄바꿈
//     return 0;  // 별 출력을 정상적으로 마치고 프로그램 종료
// }  // 이 범위 끝

// 풀이 요약
// 가로 n개의 별을 출력하고 줄을 바꾸는 작업을 세로 m번 반복하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:55:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12969_%EC%A7%81%EC%82%AC%EA%B0%81%ED%98%95_%EB%B3%84%EC%B0%8D%EA%B8%B0/README.md)
