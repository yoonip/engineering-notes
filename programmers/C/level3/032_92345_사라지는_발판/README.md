# 사라지는 발판

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92345) · Level 3 · C

## 풀이

미니맥스는 상대도 최적으로 움직인다고 보고 자신의 최선의 선택을 구하는 게임 탐색; 현재 플레이어 기준으로 이기면 최소 이동, 반드시 지면 최대 이동을 택하기
이동할 때 발판 하나를 지우고 플레이어 역할을 바꾸기; 보드 비트마스크·두 위치를 캐시 키로 써 같은 게임 상태를 재사용; 시간·공간은 도달 가능한 상태 수에 비례하며 최악에는 지수적
예: 두 플레이어가 같은 칸에 있을 때 한 명이 떠나면 그 칸이 사라져 다음 플레이어가 즉시 짐; 시작부터 이동할 곳이 없으면 이동 횟수는 0

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { uint64_t key; int value; } Entry;
typedef struct { int rows, cols; Entry* memo; size_t cap; } Context;
static int play(Context* ctx, unsigned mask, int current, int other) {
    if (!(mask & (1u << current))) return 0;
    uint64_t key = (((uint64_t)mask * 25 + current) * 25 + other) + 1;
    size_t slot = (size_t)(key * 11400714819323198485ull) & (ctx->cap - 1), probes = 0;
    while (ctx->memo[slot].key && ctx->memo[slot].key != key && probes < ctx->cap) { slot = (slot + 1) & (ctx->cap - 1); ++probes; }
    if (ctx->memo[slot].key == key) return ctx->memo[slot].value;
    int best_win = INT_MAX, best_lose = 0, r = current / ctx->cols, c = current % ctx->cols;
    const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int d = 0; d < 4; ++d) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= ctx->rows || nc < 0 || nc >= ctx->cols) continue;
        int next = nr * ctx->cols + nc; if (!(mask & (1u << next))) continue;
        int turns = play(ctx, mask ^ (1u << current), other, next) + 1;
        if (turns % 2) { if (turns < best_win) best_win = turns; }
        else if (turns > best_lose) best_lose = turns;
    }
    int answer = best_win == INT_MAX ? best_lose : best_win;
    if (probes < ctx->cap) { ctx->memo[slot].key = key; ctx->memo[slot].value = answer; }
    return answer;
}
int solution(int** board, size_t board_rows, size_t board_cols, int aloc[], size_t aloc_len, int bloc[], size_t bloc_len) {
    (void)aloc_len; (void)bloc_len; unsigned mask = 0;
    for (size_t r = 0; r < board_rows; ++r) for (size_t c = 0; c < board_cols; ++c) if (board[r][c]) mask |= 1u << (r * board_cols + c);
    size_t cap = (size_t)1 << 20; Entry* memo = calloc(cap, sizeof(*memo)); Context ctx = {(int)board_rows,(int)board_cols,memo,cap};
    int answer = play(&ctx, mask, aloc[0] * (int)board_cols + aloc[1], bloc[0] * (int)board_cols + bloc[1]); free(memo);
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
// typedef struct { uint64_t key; int value; } Entry;  // 발판과 두 위치의 메모 키를 한 상태로 묶기
// typedef struct { int rows, cols; Entry* memo; size_t cap; } Context;  // 발판 상태별 최선의 길이 / 메모 해시표 크기를 한 상태로 묶기
// static int play(Context* ctx, unsigned mask, int current, int other) {  // 보드와 메모 탐색 정보 / 아직 남은 발판 / 이번 차례 플레이어 위치 / 상대 플레이어 위치 계산용 함수
//     if (!(mask & (1u << current))) return 0;  // 현재 발판이 사라졌으면 이동할 수 없으므로 0턴
//     uint64_t key = (((uint64_t)mask * 25 + current) * 25 + other) + 1;  // 발판과 두 위치의 메모 키 갱신
//     size_t slot = (size_t)(key * 11400714819323198485ull) & (ctx->cap - 1), probes = 0;  // 메모 해시 칸 / 해시 충돌로 이동한 칸 수 저장
//     while (ctx->memo[slot].key && ctx->memo[slot].key != key && probes < ctx->cap) { slot = (slot + 1) & (ctx->cap - 1); ++probes; }  // 같은 선택 상태를 이미 계산했으면 반복; 메모 해시 칸 갱신
//     if (ctx->memo[slot].key == key) return ctx->memo[slot].value;  // 같은 선택 상태를 이미 계산했으면 발판 상태별 최선의 길이 / 메모 해시 칸로 최종값 계산
//     int best_win = INT_MAX, best_lose = 0, r = current / ctx->cols, c = current % ctx->cols;  // 이길 때의 가장 짧은 게임 길이 / 질 때의 가장 긴 게임 길이 / 현재 행 / 현재 열 저장
//     const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 행 변화 / 열 변화 저장
//     for (int d = 0; d < 4; ++d) {  // 이동 방향 순서대로 확인
//         int nr = r + dr[d], nc = c + dc[d];  // 다음 행 / 다음 열 저장
//         if (nr < 0 || nr >= ctx->rows || nc < 0 || nc >= ctx->cols) continue;  // 격자 밖이거나 막혔거나 이미 처리한 칸이면 다음 후보로 넘어가기
//         int next = nr * ctx->cols + nc; if (!(mask & (1u << next))) continue;  // 다음 발판 번호 저장
//         int turns = play(ctx, mask ^ (1u << current), other, next) + 1;  // 현재 발판을 없애고 두 플레이어의 차례를 바꿔 남은 턴 수 계산
//         if (turns % 2) { if (turns < best_win) best_win = turns; }  // 홀수 턴으로 끝나는 이기는 선택 중 가장 빨리 끝나는 값 선택
//         else if (turns > best_lose) best_lose = turns;  // 짝수 턴으로 끝나는 지는 선택 중 가장 오래 버티는 값 선택
//     }  // 이 범위 끝
//     int answer = best_win == INT_MAX ? best_lose : best_win;  // 최선의 수를 둔 게임 길이 저장
//     if (probes < ctx->cap) { ctx->memo[slot].key = key; ctx->memo[slot].value = answer; }  // 해시 칸을 찾았으면 현재 보드·두 위치 상태의 최적 턴 수 저장
//     return answer;  // 최선의 수를 둔 게임 길이 반환
// }  // 이 범위 끝
// int solution(int** board, size_t board_rows, size_t board_cols, int aloc[], size_t aloc_len, int bloc[], size_t bloc_len) {  // 미니맥스는 상대도 최적으로 움직인다고 보고 자신의 최선의 선택을 구하는 게임 탐색; 현재 플레이어 기준으로 이기면 최소 이동, 반드시 지면 최대 이동을 택하기
//     (void)aloc_len; (void)bloc_len; unsigned mask = 0;  // 아직 남은 발판 갱신
//     for (size_t r = 0; r < board_rows; ++r) for (size_t c = 0; c < board_cols; ++c) if (board[r][c]) mask |= 1u << (r * board_cols + c);  // 현재 행 순서대로 확인; 현재 열 갱신
//     size_t cap = (size_t)1 << 20; Entry* memo = calloc(cap, sizeof(*memo)); Context ctx = {(int)board_rows,(int)board_cols,memo,cap};  // 메모 해시표 크기 / 발판 상태별 최선의 길이 / 보드와 메모 탐색 정보 공간 확보하고 0으로 시작
//     int answer = play(&ctx, mask, aloc[0] * (int)board_cols + aloc[1], bloc[0] * (int)board_cols + bloc[1]); free(memo);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 최선의 수를 둔 게임 길이 반환
// }  // 이 범위 끝

// 풀이 요약
// 미니맥스는 상대도 최적으로 움직인다고 보고 자신의 최선의 선택을 구하는 게임 탐색; 현재 플레이어 기준으로 이기면 최소 이동, 반드시 지면 최대 이동을 택하기
// 이동할 때 발판 하나를 지우고 플레이어 역할을 바꾸기; 보드 비트마스크·두 위치를 캐시 키로 써 같은 게임 상태를 재사용; 시간·공간은 도달 가능한 상태 수에 비례하며 최악에는 지수적
// 예: 두 플레이어가 같은 칸에 있을 때 한 명이 떠나면 그 칸이 사라져 다음 플레이어가 즉시 짐; 시작부터 이동할 곳이 없으면 이동 횟수는 0
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/032_92345_%EC%82%AC%EB%9D%BC%EC%A7%80%EB%8A%94_%EB%B0%9C%ED%8C%90/README.md)
