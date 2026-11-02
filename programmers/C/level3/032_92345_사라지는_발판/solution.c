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
//     while (ctx->memo[slot].key && ctx->memo[slot].key != key && probes < ctx->cap) { slot = (slot + 1) & (ctx->cap - 1); ++probes; }  // 다른 키가 차지한 칸이면 다음 칸으로 이동해 같은 키 또는 빈칸 탐색
//     if (ctx->memo[slot].key == key) return ctx->memo[slot].value;  // 같은 발판·두 위치 상태의 기록이 있으면 저장한 최적 이동 수 반환
//     int best_win = INT_MAX, best_lose = 0, r = current / ctx->cols, c = current % ctx->cols;  // 이길 때의 가장 짧은 게임 길이 / 질 때의 가장 긴 게임 길이 / 현재 행 / 현재 열 저장
//     const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 행 변화 / 열 변화 저장
//     for (int d = 0; d < 4; ++d) {  // 이동 방향 순서대로 확인
//         int nr = r + dr[d], nc = c + dc[d];  // 다음 행 / 다음 열 저장
//         if (nr < 0 || nr >= ctx->rows || nc < 0 || nc >= ctx->cols) continue;  // 이동할 좌표가 격자 밖이면 해당 방향 건너뛰기
//         int next = nr * ctx->cols + nc; if (!(mask & (1u << next))) continue;  // 다음 발판 번호 저장
//         int turns = play(ctx, mask ^ (1u << current), other, next) + 1;  // 현재 발판을 없애고 두 플레이어의 차례를 바꿔 남은 턴 수 계산
//         if (turns % 2) { if (turns < best_win) best_win = turns; }  // 홀수 턴으로 끝나는 이기는 선택 중 가장 빨리 끝나는 값 선택
//         else if (turns > best_lose) best_lose = turns;  // 짝수 턴으로 끝나는 지는 선택 중 가장 오래 버티는 값 선택
//     }  // 이 범위 끝
//     int answer = best_win == INT_MAX ? best_lose : best_win;  // 최선의 수를 둔 게임 길이 저장
//     if (probes < ctx->cap) { ctx->memo[slot].key = key; ctx->memo[slot].value = answer; }  // 해시 칸을 찾았으면 현재 보드·두 위치 상태의 최적 턴 수 저장
//     return answer;  // 최선의 수를 둔 게임 길이 반환
// }  // 이 범위 끝
// int solution(int** board, size_t board_rows, size_t board_cols, int aloc[], size_t aloc_len, int bloc[], size_t bloc_len) {  // 미니맥스는 상대도 최적으로 움직인다고 가정하는 게임 탐색입니다. 이길 수 있으면 최소 이동 횟수를, 반드시 지면 최대 이동 횟수를 선택합니다.
//     (void)aloc_len; (void)bloc_len; unsigned mask = 0;  // 아직 남은 발판 갱신
//     for (size_t r = 0; r < board_rows; ++r) for (size_t c = 0; c < board_cols; ++c) if (board[r][c]) mask |= 1u << (r * board_cols + c);  // 현재 행 순서대로 확인; 현재 열 갱신
//     size_t cap = (size_t)1 << 20; Entry* memo = calloc(cap, sizeof(*memo)); Context ctx = {(int)board_rows,(int)board_cols,memo,cap};  // 메모 해시표 크기 / 발판 상태별 최선의 길이 / 보드와 메모 탐색 정보 공간 확보하고 0으로 시작
//     int answer = play(&ctx, mask, aloc[0] * (int)board_cols + aloc[1], bloc[0] * (int)board_cols + bloc[1]); free(memo);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 최선의 수를 둔 게임 길이 반환
// }  // 이 범위 끝

// 풀이 요약
// 미니맥스는 상대도 최적으로 움직인다고 가정하는 게임 탐색입니다. 이길 수 있으면 최소 이동 횟수를, 반드시 지면 최대 이동 횟수를 선택합니다.
// 이동할 때 현재 발판을 지우고 두 플레이어의 역할을 바꿉니다. 이 C 구현은 2^20칸의 고정 해시표에 발판 비트마스크와 두 위치의 결과를 저장합니다. 충돌이나 캐시 대체로 같은 상태를 다시 계산할 수 있어 시간을 고유 상태 수에만 비례한다고 볼 수 없습니다. 최악의 탐색 시간은 지수적이며, 발판 수 B에 대한 추가 공간은 O(2^20+B)입니다.
// 두 플레이어가 같은 칸에 있다면 한 명이 떠난 뒤 그 칸이 사라져 다음 플레이어가 집니다. 시작부터 이동할 수 없으면 이동 횟수는 0입니다.
