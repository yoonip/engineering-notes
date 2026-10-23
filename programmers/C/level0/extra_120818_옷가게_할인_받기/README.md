# 옷가게 할인 받기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120818) · Level 0 · C

## 풀이

가격이 큰 할인 구간부터 검사해 결제 비율 선택. 정수 곱셈과 나눗셈으로 할인 가격의 소수 부분 버림.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int price) {
    int percent = price >= 500000 ? 80 : price >= 300000 ? 90 : price >= 100000 ? 95 : 100;
    return price * percent / 100;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int price) {  // 옷가게 할인 받기 풀이 시작
//     int percent = price >= 500000 ? 80 : price >= 300000 ? 90 : price >= 100000 ? 95 : 100;  // 가격 구간별로 실제 결제 비율 선택: 80%, 90%, 95%, 100%
//     return price * percent / 100;  // 가격에 결제 비율을 곱하고 정수 나눗셈으로 소수 부분을 버려 반환
// }  // 블록 끝
// 풀이 요약
// 가격이 큰 할인 구간부터 검사해 결제 비율 선택. 정수 곱셈과 나눗셈으로 할인 가격의 소수 부분 버림.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120818_%EC%98%B7%EA%B0%80%EA%B2%8C_%ED%95%A0%EC%9D%B8_%EB%B0%9B%EA%B8%B0/README.md)
