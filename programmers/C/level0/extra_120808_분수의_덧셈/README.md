# 분수의 덧셈

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120808) · Level 0 · C

## 풀이

통분하여 더한 뒤 최대공약수로 분자와 분모를 나누어 약분

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

static int gcd(int a, int b) {
    while (b) { int r = a % b; a = b; b = r; }
    return a;
}
int* solution(int numer1, int denom1, int numer2, int denom2) {
    int n = numer1 * denom2 + numer2 * denom1;
    int d = denom1 * denom2, g = gcd(n, d);
    int* answer = malloc(2 * sizeof(*answer));
    answer[0] = n / g; answer[1] = d / g;
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
// static int gcd(int a, int b) {  // 두 정수의 최대공약수를 구하는 정수형 보조 함수를 정의
//     while (b) { int r = a % b; a = b; b = r; }  // 두 수와 나머지를 바꾸는 유클리드 호제법으로 최대공약수 계산
//     return a;  // 마지막으로 남은 0이 아닌 값인 최대공약수 반환
// }  // 블록 끝
// int* solution(int numer1, int denom1, int numer2, int denom2) {  // 분수의 덧셈 풀이 시작
//     int n = numer1 * denom2 + numer2 * denom1;  // 통분한 분자: 각 분자에 반대쪽 분모를 곱해서 합산
//     int d = denom1 * denom2, g = gcd(n, d);  // 공통 분모와 약분에 쓸 최대공약수
//     int* answer = malloc(2 * sizeof(*answer));  // answer를 저장할 메모리 확보
//     answer[0] = n / g; answer[1] = d / g;  // 분자·분모를 최대공약수로 나눠 기약분수 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 통분하여 더한 뒤 최대공약수로 분자와 분모를 나누어 약분
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:54:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120808_%EB%B6%84%EC%88%98%EC%9D%98_%EB%8D%A7%EC%85%88/README.md)
