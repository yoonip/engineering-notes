# [PCCP 기출문제] 4번 / 수레 움직이기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250134) · Level 3 · C

## 풀이

한 턴에 두 수레의 이동을 동시에 골라 DFS로 탐색; 방문 기록은 수레별로 분리하고, 같은 칸 도착·자리 교환을 금지하며 도착한 수레는 고정하기
위치뿐 아니라 두 방문 집합까지 같아야 같은 상태; 맨해튼 거리 하한으로 현재 답보다 나아질 수 없는 가지를 제거; 최악에는 가능한 방문 경로 조합을 탐색하는 지수 시간
예: 한 수레가 도착한 후에는 그 칸에서 기다리지만, 다른 수레는 그 칸을 지나갈 수 없음; 둘 모두 도착한 턴 수의 최솟값을 계산

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { uint64_t key; int turns; } Entry;
typedef struct { int rows, cols, red_goal, blue_goal, best; int** maze; Entry* memo; size_t cap; } Context;
static void search(Context* ctx, int red, int blue, unsigned red_mask, unsigned blue_mask, int turns) {
    if (red == ctx->red_goal && blue == ctx->blue_goal) { if (turns < ctx->best) ctx->best = turns; return; }
    int rd = abs(red / ctx->cols - ctx->red_goal / ctx->cols) + abs(red % ctx->cols - ctx->red_goal % ctx->cols);
    int bd = abs(blue / ctx->cols - ctx->blue_goal / ctx->cols) + abs(blue % ctx->cols - ctx->blue_goal % ctx->cols);
    if (turns + (rd > bd ? rd : bd) >= ctx->best) return;
    uint64_t key = ((uint64_t)red_mask | ((uint64_t)blue_mask << 16) | ((uint64_t)red << 32) | ((uint64_t)blue << 36)) + 1;
    size_t slot = (size_t)(key * 11400714819323198485ull) & (ctx->cap - 1), probes = 0;
    while (ctx->memo[slot].key && ctx->memo[slot].key != key && probes < ctx->cap) { slot = (slot + 1) & (ctx->cap - 1); ++probes; }
    if (ctx->memo[slot].key == key && ctx->memo[slot].turns <= turns) return;
    if (probes < ctx->cap) ctx->memo[slot] = (Entry){key,turns};
    int reds[4], blues[4], rn = 0, bn = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    if (red == ctx->red_goal) reds[rn++] = red;
    else for (int d = 0; d < 4; ++d) { int r = red / ctx->cols + dr[d], c = red % ctx->cols + dc[d]; if (r >= 0 && r < ctx->rows && c >= 0 && c < ctx->cols && ctx->maze[r][c] != 5 && !(red_mask & (1u << (r * ctx->cols + c)))) reds[rn++] = r * ctx->cols + c; }
    if (blue == ctx->blue_goal) blues[bn++] = blue;
    else for (int d = 0; d < 4; ++d) { int r = blue / ctx->cols + dr[d], c = blue % ctx->cols + dc[d]; if (r >= 0 && r < ctx->rows && c >= 0 && c < ctx->cols && ctx->maze[r][c] != 5 && !(blue_mask & (1u << (r * ctx->cols + c)))) blues[bn++] = r * ctx->cols + c; }
    for (int i = 0; i < rn; ++i) for (int j = 0; j < bn; ++j) if (reds[i] != blues[j] && !(reds[i] == blue && blues[j] == red)) search(ctx,reds[i],blues[j],red_mask | (1u << reds[i]),blue_mask | (1u << blues[j]),turns + 1);
}
int solution(int** maze, size_t maze_rows, size_t maze_cols) {
    int places[5] = {0};
    for (size_t r = 0; r < maze_rows; ++r) for (size_t c = 0; c < maze_cols; ++c) if (maze[r][c] >= 1 && maze[r][c] <= 4) places[maze[r][c]] = (int)(r * maze_cols + c);
    size_t cap = (size_t)1 << 20; Entry* memo = calloc(cap, sizeof(*memo)); int impossible = (int)(maze_rows * maze_cols) + 1;
    Context ctx = {(int)maze_rows,(int)maze_cols,places[3],places[4],impossible,maze,memo,cap}; search(&ctx,places[1],places[2],1u << places[1],1u << places[2],0); free(memo);
    return ctx.best == impossible ? 0 : ctx.best;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// typedef struct { uint64_t key; int turns; } Entry;  // 두 수레의 위치와 방문 집합 키 / 지금까지 움직인 턴를 한 상태로 묶기
// typedef struct { int rows, cols, red_goal, blue_goal, best; int** maze; Entry* memo; size_t cap; } Context;  // 같은 상태에 도달한 최소 턴 / 메모 용량를 한 상태로 묶기
// static void search(Context* ctx, int red, int blue, unsigned red_mask, unsigned blue_mask, int turns) {  // 수레의 목표와 탐색 정보 / 빨간 수레 위치 / 파란 수레 위치 / 빨간 수레가 지났던 칸 계산용 함수
//     if (red == ctx->red_goal && blue == ctx->blue_goal) { if (turns < ctx->best) ctx->best = turns; return; }  // 두 수레가 모두 도착하면 최단 턴 수를 갱신하고 탐색 종료
//     int rd = abs(red / ctx->cols - ctx->red_goal / ctx->cols) + abs(red % ctx->cols - ctx->red_goal % ctx->cols);  // 빨간 수레의 목표 최소 거리 저장
//     int bd = abs(blue / ctx->cols - ctx->blue_goal / ctx->cols) + abs(blue % ctx->cols - ctx->blue_goal % ctx->cols);  // 파란 수레의 목표 최소 거리 저장
//     if (turns + (rd > bd ? rd : bd) >= ctx->best) return;  // 남은 맨해튼 거리 하한을 더해도 현재 답 이상이면 가지치기
//     uint64_t key = ((uint64_t)red_mask | ((uint64_t)blue_mask << 16) | ((uint64_t)red << 32) | ((uint64_t)blue << 36)) + 1;  // 두 수레의 위치와 방문 집합 키 비트 상태 갱신
//     size_t slot = (size_t)(key * 11400714819323198485ull) & (ctx->cap - 1), probes = 0;  // 메모 해시 칸 / 충돌로 탐색한 칸 수 저장
//     while (ctx->memo[slot].key && ctx->memo[slot].key != key && probes < ctx->cap) { slot = (slot + 1) & (ctx->cap - 1); ++probes; }  // 같은 선택 상태를 이미 계산했으면 반복; 메모 해시 칸 갱신
//     if (ctx->memo[slot].key == key && ctx->memo[slot].turns <= turns) return;  // 같은 선택 상태를 이미 계산했으면 return
//     if (probes < ctx->cap) ctx->memo[slot] = (Entry){key,turns};  // 비어 있는 해시 칸을 찾았으면 현재 상태와 사용 턴 수 메모
//     int reds[4], blues[4], rn = 0, bn = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 빨간 수레 후보 수 / 파란 수레 후보 수 / 행 변화 / 열 변화 저장
//     if (red == ctx->red_goal) reds[rn++] = red;  // 빨강 수레가 도착했으면 현재 칸에 그대로 두기
//     else for (int d = 0; d < 4; ++d) { int r = red / ctx->cols + dr[d], c = red % ctx->cols + dc[d]; if (r >= 0 && r < ctx->rows && c >= 0 && c < ctx->cols && ctx->maze[r][c] != 5 && !(red_mask & (1u << (r * ctx->cols + c)))) reds[rn++] = r * ctx->cols + c; }  // 앞 조건이 아니면 이동 방향 / 빨간 수레 후보 수 갱신
//     if (blue == ctx->blue_goal) blues[bn++] = blue;  // 파랑 수레가 도착했으면 현재 칸에 그대로 두기
//     else for (int d = 0; d < 4; ++d) { int r = blue / ctx->cols + dr[d], c = blue % ctx->cols + dc[d]; if (r >= 0 && r < ctx->rows && c >= 0 && c < ctx->cols && ctx->maze[r][c] != 5 && !(blue_mask & (1u << (r * ctx->cols + c)))) blues[bn++] = r * ctx->cols + c; }  // 앞 조건이 아니면 이동 방향 / 파란 수레 후보 수 갱신
//     for (int i = 0; i < rn; ++i) for (int j = 0; j < bn; ++j) if (reds[i] != blues[j] && !(reds[i] == blue && blues[j] == red)) search(ctx,reds[i],blues[j],red_mask | (1u << reds[i]),blue_mask | (1u << blues[j]),turns + 1);  // 두 수레의 후보를 조합하되 같은 칸 도착과 서로 자리 바꾸기는 제외
// }  // 이 범위 끝
// int solution(int** maze, size_t maze_rows, size_t maze_cols) {  // 한 턴에 두 수레의 이동을 동시에 골라 DFS로 탐색; 방문 기록은 수레별로 분리하고, 같은 칸 도착·자리 교환을 금지하며 도착한 수레는 고정하기
//     int places[5] = {0};  // 빨강 파랑의 출발과 도착 위치 저장
//     for (size_t r = 0; r < maze_rows; ++r) for (size_t c = 0; c < maze_cols; ++c) if (maze[r][c] >= 1 && maze[r][c] <= 4) places[maze[r][c]] = (int)(r * maze_cols + c);  // 다음 후보 행 순서대로 확인; 다음 후보 열 갱신
//     size_t cap = (size_t)1 << 20; Entry* memo = calloc(cap, sizeof(*memo)); int impossible = (int)(maze_rows * maze_cols) + 1;  // 메모 용량 / 같은 상태에 도달한 최소 턴 / 목표에 못 가는 경우의 상한 공간 확보하고 0으로 시작
//     Context ctx = {(int)maze_rows,(int)maze_cols,places[3],places[4],impossible,maze,memo,cap}; search(&ctx,places[1],places[2],1u << places[1],1u << places[2],0); free(memo);  // 수레의 목표와 탐색 정보 / 빨강 파랑의 출발과 도착 위치 / 목표에 못 가는 경우의 상한 / 같은 상태에 도달한 최소 턴 임시 공간 정리
//     return ctx.best == impossible ? 0 : ctx.best;  // 수레의 목표와 탐색 정보 / 목표에 못 가는 경우의 상한로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 한 턴에 두 수레의 이동을 동시에 골라 DFS로 탐색; 방문 기록은 수레별로 분리하고, 같은 칸 도착·자리 교환을 금지하며 도착한 수레는 고정하기
// 위치뿐 아니라 두 방문 집합까지 같아야 같은 상태; 맨해튼 거리 하한으로 현재 답보다 나아질 수 없는 가지를 제거; 최악에는 가능한 방문 경로 조합을 탐색하는 지수 시간
// 예: 한 수레가 도착한 후에는 그 칸에서 기다리지만, 다른 수레는 그 칸을 지나갈 수 없음; 둘 모두 도착한 턴 수의 최솟값을 계산
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/014_250134_%5BPCCP_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_4%EB%B2%88___%EC%88%98%EB%A0%88_%EC%9B%80%EC%A7%81%EC%9D%B4%EA%B8%B0/README.md)
