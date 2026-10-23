# 점의 위치 구하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120841) · Level 0 · C

## 풀이

먼저 x의 부호로 좌우를 나누고, y의 부호로 위아래를 구분해 사분면 번호 결정.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int dot[], size_t dot_len) {
    (void)dot_len;
    return dot[0] > 0 ? (dot[1] > 0 ? 1 : 4) : (dot[1] > 0 ? 2 : 3);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int dot[], size_t dot_len) {  // 점의 위치 구하기 풀이 시작
//     (void)dot_len;  // 배열 크기처럼 함수 형식에 포함되지만 본문에서 사용하지 않는 매개변수임을 표시
//     return dot[0] > 0 ? (dot[1] > 0 ? 1 : 4) : (dot[1] > 0 ? 2 : 3);  // x가 양수면 y의 부호로 1·4사분면, x가 음수면 2·3사분면 선택
// }  // 블록 끝
// 풀이 요약
// 먼저 x의 부호로 좌우를 나누고, y의 부호로 위아래를 구분해 사분면 번호 결정.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120841_%EC%A0%90%EC%9D%98_%EC%9C%84%EC%B9%98_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
