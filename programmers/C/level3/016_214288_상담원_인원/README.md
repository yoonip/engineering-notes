# 상담원 인원

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/214288) · Level 3 · C

## 풀이

유형별 상담원 수를 바꿔 대기 시간 계산; 상담원 종료 시각 배열을 훑어 가장 먼저 비는 사람에게 다음 요청 배정
이후 유형별 인원 배정 DP로 총 n명을 나누되 각 유형에 최소 한 명 배치; L=n-k+1, 요청 수 R일 때 시간 O(kRL+RL²+kn²), 공간 O(n)
예: 첫 예제는 유형별 2·1·2명으로 배치하면 대기 합이 5+20+0=25로 최소

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int k, int n, int** reqs, size_t reqs_rows, size_t reqs_cols) {
    (void)reqs_cols; const int inf = 1000000000; int* dp = malloc(((size_t)n + 1) * sizeof(*dp)); int* next = malloc(((size_t)n + 1) * sizeof(*next));
    for (int i = 0; i <= n; ++i) dp[i] = inf; dp[0] = 0;
    int limit = n - k + 1; int* wait = malloc(((size_t)limit + 1) * sizeof(*wait)); int* ends = malloc((size_t)n * sizeof(*ends));
    for (int kind = 1; kind <= k; ++kind) {
        for (int staff = 1; staff <= limit; ++staff) {
            memset(ends, 0, (size_t)staff * sizeof(*ends)); wait[staff] = 0;
            for (size_t i = 0; i < reqs_rows; ++i) if (reqs[i][2] == kind) {
                int first = 0; for (int j = 1; j < staff; ++j) if (ends[j] < ends[first]) first = j;
                int begin = reqs[i][0] > ends[first] ? reqs[i][0] : ends[first]; wait[staff] += begin - reqs[i][0]; ends[first] = begin + reqs[i][1];
            }
        }
        for (int i = 0; i <= n; ++i) next[i] = inf;
        for (int used = 0; used <= n; ++used) if (dp[used] < inf) for (int staff = 1; staff <= limit && used + staff <= n; ++staff) if (dp[used] + wait[staff] < next[used + staff]) next[used + staff] = dp[used] + wait[staff];
        int* temp = dp; dp = next; next = temp;
    }
    int answer = dp[n]; free(dp); free(next); free(wait); free(ends);
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
// int solution(int k, int n, int** reqs, size_t reqs_rows, size_t reqs_cols) {  // 유형별 상담원 수를 바꿔 대기 시간 계산; 상담원 종료 시각 배열을 훑어 가장 먼저 비는 사람에게 다음 요청 배정
//     (void)reqs_cols; const int inf = 1000000000; int* dp = malloc(((size_t)n + 1) * sizeof(*dp)); int* next = malloc(((size_t)n + 1) * sizeof(*next));  // 지금까지 배정한 상담원 수별 최소 대기 / 새 상담 유형까지 배정한 최소 대기 공간 확보
//     for (int i = 0; i <= n; ++i) dp[i] = inf; dp[0] = 0;  // 요청 또는 DP 위치 순서대로 확인; 지금까지 배정한 상담원 수별 최소 대기 갱신
//     int limit = n - k + 1; int* wait = malloc(((size_t)limit + 1) * sizeof(*wait)); int* ends = malloc((size_t)n * sizeof(*ends));  // 한 유형에 줄 수 있는 최대 상담원 수 / 현재 유형의 인원별 대기 합 / 상담원별 마지막 종료 시각 공간 확보
//     for (int kind = 1; kind <= k; ++kind) {  // 현재 상담 유형 순서대로 확인
//         for (int staff = 1; staff <= limit; ++staff) {  // 이 유형에 둘 상담원 수 순서대로 확인
//             memset(ends, 0, (size_t)staff * sizeof(*ends)); wait[staff] = 0;  // 현재 유형의 인원별 대기 합 초기화
//             for (size_t i = 0; i < reqs_rows; ++i) if (reqs[i][2] == kind) {  // 현재 상담 유형의 요청만 시간 순서대로 처리
//                 int first = 0; for (int j = 1; j < staff; ++j) if (ends[j] < ends[first]) first = j;  // 종료 시각 배열에서 가장 먼저 비는 상담원 찾기
//                 int begin = reqs[i][0] > ends[first] ? reqs[i][0] : ends[first]; wait[staff] += begin - reqs[i][0]; ends[first] = begin + reqs[i][1];  // 현재 요청의 실제 시작 시각 / 상담원별 마지막 종료 시각 저장
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         for (int i = 0; i <= n; ++i) next[i] = inf;  // 요청 또는 DP 위치 순서대로 확인; 새 상담 유형까지 배정한 최소 대기 갱신
//         for (int used = 0; used <= n; ++used) if (dp[used] < inf) for (int staff = 1; staff <= limit && used + staff <= n; ++staff) if (dp[used] + wait[staff] < next[used + staff]) next[used + staff] = dp[used] + wait[staff];  // 앞 유형까지의 최소 대기에 현재 유형 인원별 대기를 더해 최솟값 갱신
//         int* temp = dp; dp = next; next = temp;  // DP 배열 교환용 포인터 / 지금까지 배정한 상담원 수별 최소 대기 / 새 상담 유형까지 배정한 최소 대기 저장
//     }  // 이 범위 끝
//     int answer = dp[n]; free(dp); free(next); free(wait); free(ends);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 모든 인원을 배정한 최소 대기 반환
// }  // 이 범위 끝

// 풀이 요약
// 유형별 상담원 수를 바꿔 대기 시간 계산; 상담원 종료 시각 배열을 훑어 가장 먼저 비는 사람에게 다음 요청 배정
// 이후 유형별 인원 배정 DP로 총 n명을 나누되 각 유형에 최소 한 명 배치; L=n-k+1, 요청 수 R일 때 시간 O(kRL+RL²+kn²), 공간 O(n)
// 예: 첫 예제는 유형별 2·1·2명으로 배치하면 대기 합이 5+20+0=25로 최소
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:28:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/016_214288_%EC%83%81%EB%8B%B4%EC%9B%90_%EC%9D%B8%EC%9B%90/README.md)
