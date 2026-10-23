# 유한소수 판별하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120878) · Level 0 · C

## 풀이

약분한 분모에서 2와 5를 모두 제거했을 때 1이 남으면 유한소수임

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int a, int b) {
    int x = a, y = b;
    while (y) { int r = x % y; x = y; y = r; }
    b /= x;
    while (b % 2 == 0) b /= 2;
    while (b % 5 == 0) b /= 5;
    return b == 1 ? 1 : 2;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int a, int b) {  // 유한소수 판별하기 풀이 시작
//     int x = a, y = b;  // 최대공약수를 구하는 동안 원래 분수 값을 보존할 복사본
//     while (y) { int r = x % y; x = y; y = r; }  // 유클리드 호제법으로 나머지를 반복 계산해 최대공약수 x 구하기
//     b /= x;  // 분모를 최대공약수로 나누어 기약분수의 분모로 약분
//     while (b % 2 == 0) b /= 2;  // while은 분모가 해당 소인수로 나누어지는 동안 반복하여 그 소인수를 제거
//     while (b % 5 == 0) b /= 5;  // while은 분모가 해당 소인수로 나누어지는 동안 반복하여 그 소인수를 제거
//     return b == 1 ? 1 : 2;  // 약분한 분모에서 2와 5를 모두 없앤 뒤 1이면 유한소수 1, 아니면 2 반환
// }  // 블록 끝
// 풀이 요약
// 약분한 분모에서 2와 5를 모두 제거했을 때 1이 남으면 유한소수임
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120878_%EC%9C%A0%ED%95%9C%EC%86%8C%EC%88%98_%ED%8C%90%EB%B3%84%ED%95%98%EA%B8%B0/README.md)
