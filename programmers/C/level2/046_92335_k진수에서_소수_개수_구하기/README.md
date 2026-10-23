# k진수에서 소수 개수 구하기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92335) · Level 2 · C

## 풀이

k진수로 변환한 문자열을 0으로 나누면 필요한 경계 조건을 만족하는 후보만 남음; 각 후보를 10진수로 읽어 소수 판정하기
예: 437674의 3진수에서 211·2·11이 남아 3개.; 후보 값 p에 대해 소수 검사는 O(√p), 변환 문자열 공간 O(log_k n)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static bool is_prime(long long value) {
    if (value < 2) return false;
    if (value % 2 == 0) return value == 2;
    for (long long d = 3; d <= value / d; d += 2) if (value % d == 0) return false;
    return true;
}
int solution(int n, int k) {
    char digits[64]; int len = 0, answer = 0;
    while (n) { digits[len++] = '0' + n % k; n /= k; }
    long long value = 0;
    for (int i = len - 1; i >= -1; --i) {
        if (i >= 0 && digits[i] != '0') value = value * 10 + digits[i] - '0';
        else { answer += is_prime(value); value = 0; }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static bool is_prime(long long value) {  // 홀수 약수만 확인해서 소수 판정
//     if (value < 2) return false;  // 0 사이에서 읽고 있는 십진 정수가 2보다 작으면 조건을 못 지켰으니 실패
//     if (value % 2 == 0) return value == 2;  // 짝수 중 소수는 2뿐이므로 2인지 바로 반환
//     for (long long d = 3; d <= value / d; d += 2) if (value % d == 0) return false;  // 3부터 홀수 약수만 검사하고 나누어떨어지면 소수가 아님
//     return true;  // 끝까지 조건을 지켰으니 성공
// }  // 이 범위 끝
// int solution(int n, int k) {  // k진수로 변환한 문자열을 0으로 나누면 필요한 경계 조건을 만족하는 후보만 남음; 각 후보를 10진수로 읽어 소수 판정하기
//     char digits[64]; int len = 0, answer = 0;  // k진수의 길이 / 소수인 구간 수 저장
//     while (n) { digits[len++] = '0' + n % k; n /= k; }  // k로 나눈 나머지를 거꾸로 기록하며 k진수 자릿수 생성
//     long long value = 0;  // 0 사이에서 읽고 있는 십진 정수 저장
//     for (int i = len - 1; i >= -1; --i) {  // 왼쪽부터 읽을 k진수 위치 순서대로 확인
//         if (i >= 0 && digits[i] != '0') value = value * 10 + digits[i] - '0';  // 0이 아닌 숫자는 현재 진법 조각에 이어 붙이기
//         else { answer += is_prime(value); value = 0; }  // 앞 조건이 아니면 소수인 구간 수 / 0 사이에서 읽고 있는 십진 정수 더해 누적
//     }  // 이 범위 끝
//     return answer;  // 소수인 구간 수 반환
// }  // 이 범위 끝

// 풀이 요약
// k진수로 변환한 문자열을 0으로 나누면 필요한 경계 조건을 만족하는 후보만 남음; 각 후보를 10진수로 읽어 소수 판정하기
// 예: 437674의 3진수에서 211·2·11이 남아 3개.; 후보 값 p에 대해 소수 검사는 O(√p), 변환 문자열 공간 O(log_k n)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/046_92335_k%EC%A7%84%EC%88%98%EC%97%90%EC%84%9C_%EC%86%8C%EC%88%98_%EA%B0%9C%EC%88%98_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
