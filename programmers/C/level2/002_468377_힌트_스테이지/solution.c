#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

typedef struct { int** cost; int** hint; int n; int hint_cols; int* tickets; int answer; } Context;
static void search(Context* ctx, int stage, int total) {
    int discount = ctx->tickets[stage]; if (discount >= ctx->n) discount = ctx->n - 1;
    total += ctx->cost[stage][discount];
    if (total >= ctx->answer) return;
    if (stage == ctx->n - 1) { ctx->answer = total; return; }
    search(ctx, stage + 1, total);
    for (int j = 1; j < ctx->hint_cols; ++j) ++ctx->tickets[ctx->hint[stage][j] - 1];
    search(ctx, stage + 1, total + ctx->hint[stage][0]);
    for (int j = 1; j < ctx->hint_cols; ++j) --ctx->tickets[ctx->hint[stage][j] - 1];
}
int solution(int** cost, size_t cost_rows, size_t cost_cols, int** hint, size_t hint_rows, size_t hint_cols) {
    (void)cost_cols; (void)hint_rows;
    int* tickets = calloc(cost_rows, sizeof(*tickets)); int upper = 0;
    for (size_t i = 0; i < cost_rows; ++i) upper += cost[i][0];
    Context ctx = {cost,hint,(int)cost_rows,(int)hint_cols,tickets,upper}; search(&ctx, 0, 0); free(tickets);
    return ctx.answer;
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
// typedef struct { int** cost; int** hint; int n; int hint_cols; int* tickets; int answer; } Context;  // 스테이지별 할인권 수 / 끝까지 진행하는 최소 비용를 한 상태로 묶기
// static void search(Context* ctx, int stage, int total) {  // 힌트와 가격 탐색 정보 / 현재 스테이지 번호 / 현재 경로의 누적 비용 계산용 함수
//     int discount = ctx->tickets[stage]; if (discount >= ctx->n) discount = ctx->n - 1;  // 현재 스테이지에 쌓인 할인권 수 저장
//     total += ctx->cost[stage][discount];  // 현재 경로의 누적 비용 / 현재 스테이지 번호 / 현재 스테이지에 쌓인 할인권 수 더해 누적
//     if (total >= ctx->answer) return;  // 이미 구한 최솟값 이상을 썼으면 더 진행해도 유리하지 않으므로 가지치기
//     if (stage == ctx->n - 1) { ctx->answer = total; return; }  // 마지막 스테이지까지 왔으면 최소 비용을 현재 누적값으로 갱신
//     search(ctx, stage + 1, total);  // 정한 선택을 반영한 다음 상태로 재귀 탐색을 진행하기
//     for (int j = 1; j < ctx->hint_cols; ++j) ++ctx->tickets[ctx->hint[stage][j] - 1];  // 구매한 힌트의 적용 스테이지 위치 순서대로 확인; 힌트와 가격 탐색 정보 갱신
//     search(ctx, stage + 1, total + ctx->hint[stage][0]);  // 정한 선택을 반영한 다음 상태로 재귀 탐색을 진행하기
//     for (int j = 1; j < ctx->hint_cols; ++j) --ctx->tickets[ctx->hint[stage][j] - 1];  // 구매한 힌트의 적용 스테이지 위치 순서대로 확인; 힌트와 가격 탐색 정보 갱신
// }  // 이 범위 끝
// int solution(int** cost, size_t cost_rows, size_t cost_cols, int** hint, size_t hint_rows, size_t hint_cols) {  // 각 단계에서 힌트 구매/미구매를 DFS(깊이 우선 탐색)로 비교
//     (void)cost_cols; (void)hint_rows;  // (void)cost_cols; (void)hint_rows
//     int* tickets = calloc(cost_rows, sizeof(*tickets)); int upper = 0;  // 스테이지별 할인권 수 / 힌트를 안 산 기본 비용 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < cost_rows; ++i) upper += cost[i][0];  // 기본 가격을 더할 스테이지 순서대로 확인; 힌트를 안 산 기본 비용 / 기본 가격을 더할 스테이지 더해 누적
//     Context ctx = {cost,hint,(int)cost_rows,(int)hint_cols,tickets,upper}; search(&ctx, 0, 0); free(tickets);  // 힌트와 가격 탐색 정보 / 스테이지별 할인권 수 / 힌트를 안 산 기본 비용 임시 공간 정리
//     return ctx.answer;  // 힌트와 가격 탐색 정보 / 끝까지 진행하는 최소 비용로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 각 단계에서 힌트 구매/미구매를 DFS(깊이 우선 탐색)로 비교
// 티켓은 다음 단계에 적용하고, 탐색 후 되돌리기; 모든 선택 중 최소 비용을 반환
// 예: 티켓이 0장이면 cost[i][0], 1장이면 cost[i][1]의 비용을 내기
