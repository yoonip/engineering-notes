#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

typedef struct { int** users; size_t user_count; int* prices; size_t item_count; int* rates; int subscribers; int revenue; } Context;
static void search(Context* ctx, size_t index) {
    if (index < ctx->item_count) {
        for (int rate = 10; rate <= 40; rate += 10) { ctx->rates[index] = rate; search(ctx, index + 1); }
        return;
    }
    int subscribers = 0, revenue = 0;
    for (size_t i = 0; i < ctx->user_count; ++i) {
        int cost = 0;
        for (size_t j = 0; j < ctx->item_count; ++j) if (ctx->rates[j] >= ctx->users[i][0]) cost += ctx->prices[j] * (100 - ctx->rates[j]) / 100;
        if (cost >= ctx->users[i][1]) ++subscribers; else revenue += cost;
    }
    if (subscribers > ctx->subscribers || (subscribers == ctx->subscribers && revenue > ctx->revenue)) { ctx->subscribers = subscribers; ctx->revenue = revenue; }
}
int* solution(int** users, size_t users_rows, size_t users_cols, int emoticons[], size_t emoticons_len) {
    (void)users_cols;
    int* rates = malloc(emoticons_len * sizeof(*rates)); Context ctx = {users,users_rows,emoticons,emoticons_len,rates,0,0};
    search(&ctx, 0); free(rates); int* answer = malloc(2 * sizeof(*answer));
    answer[0] = ctx.subscribers; answer[1] = ctx.revenue;
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
// typedef struct { int** users; size_t user_count; int* prices; size_t item_count; int* rates; int subscribers; int revenue; } Context;  // 선택한 이모티콘별 할인율 / 현재 할인 조합의 가입자 수 / 가입하지 않은 사용자의 구매 금액를 한 상태로 묶기
// static void search(Context* ctx, size_t index) {  // 할인 조합 탐색 정보 / 할인율을 정할 이모티콘 계산용 함수
//     if (index < ctx->item_count) {  // 아직 할인율을 정하지 않은 이모티콘이 있으면 다음 할인 선택으로 진행
//         for (int rate = 10; rate <= 40; rate += 10) { ctx->rates[index] = rate; search(ctx, index + 1); }  // 이번에 선택할 할인율 순서대로 확인; 선택한 이모티콘별 할인율로 다음 선택 탐색
//         return;  // 현재 분기의 계산을 끝내고 이전 단계로 복귀
//     }  // 이 범위 끝
//     int subscribers = 0, revenue = 0;  // 현재 할인 조합의 가입자 수 / 가입하지 않은 사용자의 구매 금액 저장
//     for (size_t i = 0; i < ctx->user_count; ++i) {  // 사용자 번호 순서대로 확인
//         int cost = 0;  // 현재 사용자가 구매할 금액 저장
//         for (size_t j = 0; j < ctx->item_count; ++j) if (ctx->rates[j] >= ctx->users[i][0]) cost += ctx->prices[j] * (100 - ctx->rates[j]) / 100;  // 사용자가 원하는 할인율 이상인 상품만 할인 가격으로 구매액에 합산
//         if (cost >= ctx->users[i][1]) ++subscribers; else revenue += cost;  // 구매액이 가입 기준 이상이면 가입자 수에, 아니면 매출에 반영
//     }  // 이 범위 끝
//     if (subscribers > ctx->subscribers || (subscribers == ctx->subscribers && revenue > ctx->revenue)) { ctx->subscribers = subscribers; ctx->revenue = revenue; }  // 가입자 수가 더 많거나 동률에서 매출이 더 높을 때 최선 조합 교체
// }  // 이 범위 끝
// int* solution(int** users, size_t users_rows, size_t users_cols, int emoticons[], size_t emoticons_len) {  // 할인율 4가지의 모든 조합을 평가해 사용자별 가입 또는 구매 결과를 합산하기; (가입자,매출)의 사전식 최댓값을 선택
//     (void)users_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* rates = malloc(emoticons_len * sizeof(*rates)); Context ctx = {users,users_rows,emoticons,emoticons_len,rates,0,0};  // 선택한 이모티콘별 할인율 / 할인 조합 탐색 정보 공간 확보
//     search(&ctx, 0); free(rates); int* answer = malloc(2 * sizeof(*answer));  // 최대 가입자 수와 그때의 매출 공간 확보
//     answer[0] = ctx.subscribers; answer[1] = ctx.revenue;  // 최대 가입자 수와 그때의 매출 갱신
//     return answer;  // 최대 가입자 수와 그때의 매출 반환
// }  // 이 범위 끝

// 풀이 요약
// 할인율 4가지의 모든 조합을 평가해 사용자별 가입 또는 구매 결과를 합산하기; (가입자,매출)의 사전식 최댓값을 선택
// 예: 첫 예제는 30%,40% 할인으로 [1,5400]; 사용자 N명·이모티콘 M개일 때 시간 O(4^M*N*M), 추가 공간 O(M)
