# 억억단을 외우자

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/138475) · Level 3 · C

## 풀이

정수 x가 곱셈표에 나오는 횟수는 x의 약수 개수; 소인수 지수가 a일 때 약수 선택 수 a+1을 곱하는 체로 개수를 계산
시작점을 내림차순으로 처리하면 오른쪽부터 구간을 늘리며 한 번만 스캔할 수 있음; 같은 약수 개수면 더 작은 수로 갱신; 시간 O(E log log E+Q log Q), 공간 O(E+Q)
예: 1~8에서 6과 8의 약수는 네 개로 최다; [1,8]·[3,8]은 작은 수 6, [7,8]은 8이 답

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int* solution(int e, int starts[], size_t starts_len) {
    int* divisors = malloc(((size_t)e + 1) * sizeof(*divisors)); int* winner = malloc(((size_t)e + 1) * sizeof(*winner));
    for (int i = 0; i <= e; ++i) divisors[i] = 1;
    for (int prime = 2; prime <= e; ++prime) if (divisors[prime] == 1) {
        long long power = prime; int exponent = 1;
        while (power <= e) { for (int multiple = (int)power; multiple <= e; multiple += (int)power) divisors[multiple] = divisors[multiple] / exponent * (exponent + 1); power *= prime; ++exponent; }
    }
    int best = e;
    for (int i = e; i >= 1; --i) { if (divisors[i] >= divisors[best]) best = i; winner[i] = best; }
    int* answer = malloc(starts_len * sizeof(*answer)); for (size_t i = 0; i < starts_len; ++i) answer[i] = winner[starts[i]];
    free(divisors); free(winner);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int* solution(int e, int starts[], size_t starts_len) {  // 정수 x가 곱셈표에 나오는 횟수는 x의 약수 개수; 소인수 지수가 a일 때 약수 선택 수 a+1을 곱하는 체로 개수를 계산
//     int* divisors = malloc(((size_t)e + 1) * sizeof(*divisors)); int* winner = malloc(((size_t)e + 1) * sizeof(*winner));  // 정수별 약수 개수 / 각 시작 이상에서 최선인 정수 공간 확보
//     for (int i = 0; i <= e; ++i) divisors[i] = 1;  // 뒤에서 확인할 정수 또는 질의 순서대로 확인; 정수별 약수 개수 갱신
//     for (int prime = 2; prime <= e; ++prime) if (divisors[prime] == 1) {  // 아직 약수 정보가 없는 수를 소수로 잡아 배수의 약수 수 계산
//         long long power = prime; int exponent = 1;  // 현재 소수 거듭제곱 / 해당 소수의 지수 저장
//         while (power <= e) { for (int multiple = (int)power; multiple <= e; multiple += (int)power) divisors[multiple] = divisors[multiple] / exponent * (exponent + 1); power *= prime; ++exponent; }  // 소수 거듭제곱의 배수마다 해당 소수 지수에 따른 약수 수 갱신
//     }  // 이 범위 끝
//     int best = e;  // 지금까지 약수가 가장 많은 정수 저장
//     for (int i = e; i >= 1; --i) { if (divisors[i] >= divisors[best]) best = i; winner[i] = best; }  // 뒤에서 확인할 정수 또는 질의 순서대로 확인; 지금까지 약수가 가장 많은 정수 / 각 시작 이상에서 최선인 정수 갱신
//     int* answer = malloc(starts_len * sizeof(*answer)); for (size_t i = 0; i < starts_len; ++i) answer[i] = winner[starts[i]];  // 시작값별 최선의 정수 / 뒤에서 확인할 정수 또는 질의 공간 확보
//     free(divisors); free(winner);  // 정수별 약수 개수 / 각 시작 이상에서 최선인 정수 임시 공간 정리
//     return answer;  // 시작값별 최선의 정수 반환
// }  // 이 범위 끝

// 풀이 요약
// 정수 x가 곱셈표에 나오는 횟수는 x의 약수 개수; 소인수 지수가 a일 때 약수 선택 수 a+1을 곱하는 체로 개수를 계산
// 시작점을 내림차순으로 처리하면 오른쪽부터 구간을 늘리며 한 번만 스캔할 수 있음; 같은 약수 개수면 더 작은 수로 갱신; 시간 O(E log log E+Q log Q), 공간 O(E+Q)
// 예: 1~8에서 6과 8의 약수는 네 개로 최다; [1,8]·[3,8]은 작은 수 6, [7,8]은 8이 답
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/023_138475_%EC%96%B5%EC%96%B5%EB%8B%A8%EC%9D%84_%EC%99%B8%EC%9A%B0%EC%9E%90/README.md)
