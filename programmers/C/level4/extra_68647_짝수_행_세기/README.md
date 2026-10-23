# 짝수 행 세기

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68647) · Level 4 · C

## 풀이

열별 1의 개수만 고정되어 있으므로, 행의 구체적인 모양 대신 짝수 합인 행 개수만 DP 상태로 저장
이번 열에 1을 놓은 행은 짝수↔홀수가 바뀜; 각 그룹에서 고르는 행의 조합 수를 곱해 전이하기
예: 한 행의 합이 0이어도 짝수; 행 R, 열 C일 때 시간 O(C*R^2), 공간 O(R^2)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int** a, size_t a_rows, size_t a_cols) {
    const int mod = 10000019; int n = (int)a_rows; size_t stride = a_rows + 1;
    int* choose = calloc(stride * stride, sizeof(*choose)); int* dp = calloc(stride, sizeof(*dp)); int* next = malloc(stride * sizeof(*next));
    for (int total = 0; total <= n; ++total) { choose[total * stride] = choose[total * stride + total] = 1; for (int selected = 1; selected < total; ++selected) choose[total * stride + selected] = (choose[(total - 1) * stride + selected - 1] + choose[(total - 1) * stride + selected]) % mod; }
    dp[n] = 1;
    for (size_t column = 0; column < a_cols; ++column) {
        int ones = 0; for (int row = 0; row < n; ++row) ones += a[row][column]; memset(next,0,stride * sizeof(*next));
        for (int even = 0; even <= n; ++even) if (dp[even]) {
            int low = ones - (n - even); if (low < 0) low = 0; int high = even < ones ? even : ones;
            for (int changed = low; changed <= high; ++changed) {
                int new_even = even + ones - 2 * changed;
                long long ways = (long long)dp[even] * choose[even * stride + changed] % mod * choose[(n - even) * stride + ones - changed] % mod;
                next[new_even] = (int)((next[new_even] + ways) % mod);
            }
        }
        int* temp = dp; dp = next; next = temp;
    }
    int answer = dp[n]; free(choose); free(dp); free(next);
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
// int solution(int** a, size_t a_rows, size_t a_cols) {  // 열별 1의 개수만 고정되어 있으므로, 행의 구체적인 모양 대신 짝수 합인 행 개수만 DP 상태로 저장
//     const int mod = 10000019; int n = (int)a_rows; size_t stride = a_rows + 1;  // 전체 행 수 / 이항계수 표 한 행 길이 저장
//     int* choose = calloc(stride * stride, sizeof(*choose)); int* dp = calloc(stride, sizeof(*dp)); int* next = malloc(stride * sizeof(*next));  // 행을 고르는 이항계수 표 / 짝수 행 개수별 현재 경우의 수 / 다음 열까지 채운 경우의 수 공간 확보하고 0으로 시작
//     for (int total = 0; total <= n; ++total) { choose[total * stride] = choose[total * stride + total] = 1; for (int selected = 1; selected < total; ++selected) choose[total * stride + selected] = (choose[(total - 1) * stride + selected - 1] + choose[(total - 1) * stride + selected]) % mod; }  // 파스칼 점화식으로 행을 고르는 이항계수 표 계산
//     dp[n] = 1;  // 아직 열을 채우기 전에는 모든 행의 합이 0인 짝수 상태 한 가지
//     for (size_t column = 0; column < a_cols; ++column) {  // 추가할 열 순서대로 확인
//         int ones = 0; for (int row = 0; row < n; ++row) ones += a[row][column]; memset(next,0,stride * sizeof(*next));  // 이번 열의 1 개수를 세고 다음 열 DP 배열을 0으로 비우기
//         for (int even = 0; even <= n; ++even) if (dp[even]) {  // 가능한 짝수 행 개수 상태에서 이번 열의 1 배치로 전이
//             int low = ones - (n - even); if (low < 0) low = 0; int high = even < ones ? even : ones;  // 짝수 행에서 고를 최소 개수 / 짝수 행에서 고를 최대 개수 저장
//             for (int changed = low; changed <= high; ++changed) {  // 짝수 행에 새로 놓을 1 개수 순서대로 확인
//                 int new_even = even + ones - 2 * changed;  // 새 열 뒤의 짝수 행 수 저장
//                 long long ways = (long long)dp[even] * choose[even * stride + changed] % mod * choose[(n - even) * stride + ones - changed] % mod;  // 짝수 행과 홀수 행에서 고르는 조합 수 저장
//                 next[new_even] = (int)((next[new_even] + ways) % mod);  // 다음 열까지 채운 경우의 수 갱신
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         int* temp = dp; dp = next; next = temp;  // DP 배열 교환용 포인터 / 짝수 행 개수별 현재 경우의 수 / 다음 열까지 채운 경우의 수 저장
//     }  // 이 범위 끝
//     int answer = dp[n]; free(choose); free(dp); free(next);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 마지막에 모든 행이 짝수인 경우의 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 열별 1의 개수만 고정되어 있으므로, 행의 구체적인 모양 대신 짝수 합인 행 개수만 DP 상태로 저장
// 이번 열에 1을 놓은 행은 짝수↔홀수가 바뀜; 각 그룹에서 고르는 행의 조합 수를 곱해 전이하기
// 예: 한 행의 합이 0이어도 짝수; 행 R, 열 C일 때 시간 O(C*R^2), 공간 O(R^2)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:38:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_68647_%EC%A7%9D%EC%88%98_%ED%96%89_%EC%84%B8%EA%B8%B0/README.md)
