# 팩토리얼

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120848) · Level 0 · C

## 풀이

현재 팩토리얼에 다음 차수를 곱해도 n 이하일 때만 차수를 증가. n 이하인 가장 큰 팩토리얼의 차수 반환.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int factorial = 1, answer = 1;
    while (factorial <= n / (answer + 1)) factorial *= ++answer;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) {  // 팩토리얼 풀이 시작
//     int factorial = 1, answer = 1;  // 현재 팩토리얼과 n을 넘지 않는 최대 차수. 둘 다 1부터 확인
//     while (factorial <= n / (answer + 1)) factorial *= ++answer;  // 다음 팩토리얼이 n 이하일 때만 차수를 늘려 곱함. 나눗셈으로 비교해 먼저 큰 수를 곱하는 일을 피함
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 현재 팩토리얼에 다음 차수를 곱해도 n 이하일 때만 차수를 증가. n 이하인 가장 큰 팩토리얼의 차수 반환.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120848_%ED%8C%A9%ED%86%A0%EB%A6%AC%EC%96%BC/README.md)
