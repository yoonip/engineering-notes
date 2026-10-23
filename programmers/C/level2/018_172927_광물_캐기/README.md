# 광물 캐기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/172927) · Level 2 · C

## 풀이

광물을 순서대로 다섯 개씩 묶고, 각 묶음에 쓸 곡괭이를 모두 선택해 보기; 남은 수가 같은 상태는 캐시로 재사용
예: 첫 묶음은 다이아, 나머지는 철 곡괭이를 쓰면 12.; 묶음 수 B, 초기 곡괭이 수 D,I,S일 때 시간·공간 O(B(D+1)(I+1)(S+1))

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

typedef struct { int (*blocks)[3]; size_t count; int initial; int b_size; int c_size; int* memo; } Context;
static int search(Context* ctx, int a, int b, int c) {
    size_t index = (size_t)(ctx->initial - a - b - c);
    if (index >= ctx->count || a + b + c == 0) return 0;
    size_t key = ((size_t)a * ctx->b_size + b) * ctx->c_size + c;
    if (ctx->memo[key] >= 0) return ctx->memo[key];
    int best = INT_MAX, value;
    if (a) { value = ctx->blocks[index][0] + search(ctx, a - 1, b, c); if (value < best) best = value; }
    if (b) { value = ctx->blocks[index][1] + search(ctx, a, b - 1, c); if (value < best) best = value; }
    if (c) { value = ctx->blocks[index][2] + search(ctx, a, b, c - 1); if (value < best) best = value; }
    ctx->memo[key] = best;
    return best;
}
int solution(int picks[], size_t picks_len, const char* minerals[], size_t minerals_len) {
    (void)picks_len;
    size_t count = (minerals_len + 4) / 5; int (*blocks)[3] = calloc(count, sizeof(*blocks));
    for (size_t i = 0; i < minerals_len; ++i) {
        int kind = !strcmp(minerals[i], "diamond") ? 0 : !strcmp(minerals[i], "iron") ? 1 : 2;
        const int fatigue[3][3] = {{1,5,25},{1,1,5},{1,1,1}};
        for (int pick = 0; pick < 3; ++pick) blocks[i / 5][pick] += fatigue[kind][pick];
    }
    size_t states = (size_t)(picks[0] + 1) * (picks[1] + 1) * (picks[2] + 1); int* memo = malloc(states * sizeof(*memo));
    for (size_t i = 0; i < states; ++i) memo[i] = -1;
    Context ctx = {blocks,count,picks[0] + picks[1] + picks[2],picks[1] + 1,picks[2] + 1,memo};
    int answer = search(&ctx, picks[0], picks[1], picks[2]); free(blocks); free(memo);
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
// typedef struct { int (*blocks)[3]; size_t count; int initial; int b_size; int c_size; int* memo; } Context;  // 묶음별 곡괭이 종류에 따른 피로도 / 광물 묶음 수 / 남은 곡괭이 조합별 최소 피로도를 한 상태로 묶기
// static int search(Context* ctx, int a, int b, int c) {  // 남은 세 종류 곡괭이 수를 상태로 최소 피로도 탐색
//     size_t index = (size_t)(ctx->initial - a - b - c);  // 처음 곡괭이 수에서 남은 수를 빼 다음에 캘 묶음 번호 계산
//     if (index >= ctx->count || a + b + c == 0) return 0;  // 묶음을 다 캤거나 곡괭이를 다 썼으면 추가 피로도는 0
//     size_t key = ((size_t)a * ctx->b_size + b) * ctx->c_size + c;  // 남은 다이아·철·돌 곡괭이 수를 일차원 메모 번호로 변환
//     if (ctx->memo[key] >= 0) return ctx->memo[key];  // 같은 곡괭이 조합을 계산했다면 저장한 최소 피로도 재사용
//     int best = INT_MAX, value;  // 앞으로 캘 때 최소 피로도 저장
//     if (a) { value = ctx->blocks[index][0] + search(ctx, a - 1, b, c); if (value < best) best = value; }  // 다이아 곡괭이로 현재 묶음을 캔 피로도와 나머지 최솟값 비교
//     if (b) { value = ctx->blocks[index][1] + search(ctx, a, b - 1, c); if (value < best) best = value; }  // 철 곡괭이로 현재 묶음을 캔 피로도와 나머지 최솟값 비교
//     if (c) { value = ctx->blocks[index][2] + search(ctx, a, b, c - 1); if (value < best) best = value; }  // 돌 곡괭이로 현재 묶음을 캔 피로도와 나머지 최솟값 비교
//     ctx->memo[key] = best;  // 남은 곡괭이 조합별 최소 피로도 갱신
//     return best;  // 앞으로 캘 때 최소 피로도 반환
// }  // 이 범위 끝
// int solution(int picks[], size_t picks_len, const char* minerals[], size_t minerals_len) {  // 광물을 순서대로 다섯 개씩 묶고, 각 묶음에 쓸 곡괭이를 모두 선택해 보기; 남은 수가 같은 상태는 캐시로 재사용
//     (void)picks_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     size_t count = (minerals_len + 4) / 5; int (*blocks)[3] = calloc(count, sizeof(*blocks));  // 광물 묶음 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < minerals_len; ++i) {  // 광물 또는 메모 위치 순서대로 확인
//         int kind = !strcmp(minerals[i], "diamond") ? 0 : !strcmp(minerals[i], "iron") ? 1 : 2;  // 현재 광물 종류 저장
//         const int fatigue[3][3] = {{1,5,25},{1,1,5},{1,1,1}};  // 광물과 곡괭이 종류별 피로도 저장
//         for (int pick = 0; pick < 3; ++pick) blocks[i / 5][pick] += fatigue[kind][pick];  // 현재 광물 한 개의 피로도를 세 종류 곡괭이별 묶음 비용에 더하기
//     }  // 이 범위 끝
//     size_t states = (size_t)(picks[0] + 1) * (picks[1] + 1) * (picks[2] + 1); int* memo = malloc(states * sizeof(*memo));  // 메모할 곡괭이 조합 수 / 남은 곡괭이 조합별 최소 피로도 공간 확보
//     for (size_t i = 0; i < states; ++i) memo[i] = -1;  // 메모를 -1로 채워 아직 계산하지 않은 조합 표시
//     Context ctx = {blocks,count,picks[0] + picks[1] + picks[2],picks[1] + 1,picks[2] + 1,memo};  // 광물 묶음과 곡괭이 탐색 정보 저장
//     int answer = search(&ctx, picks[0], picks[1], picks[2]); free(blocks); free(memo);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 전체 최소 피로도 반환
// }  // 이 범위 끝

// 풀이 요약
// 광물을 순서대로 다섯 개씩 묶고, 각 묶음에 쓸 곡괭이를 모두 선택해 보기; 남은 수가 같은 상태는 캐시로 재사용
// 예: 첫 묶음은 다이아, 나머지는 철 곡괭이를 쓰면 12.; 묶음 수 B, 초기 곡괭이 수 D,I,S일 때 시간·공간 O(B(D+1)(I+1)(S+1))
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:10:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/018_172927_%EA%B4%91%EB%AC%BC_%EC%BA%90%EA%B8%B0/README.md)
