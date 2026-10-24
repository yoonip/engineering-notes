# 가장 큰 삼각형 덩어리

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389629) · Level 4 · C

## 풀이

삼각형은 두 바깥 변으로만 연결되어 이웃이 최대 2개; 따라서 전체 그래프는 경로 또는 고리로 나뉨

덩어리는 그 위의 연속 구간이며, 같은 정사각형의 삼각형 두 개를 함께 고를 수 없으므로 중복 칸 없는 최장 구간을 찾기

예: [[1]]은 넓이 1; 고리는 두 번 이어 경계를 넘는 구간도 확인; 시간·공간 O(N*M)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int (*neighbors)[2]; unsigned char* degree; bool* seen; int* order; int* last; int* stamp; int component; int best; } Context;
static void inspect(Context* ctx, int start) {
    int previous = -1, current = start, length = 0;
    while (!ctx->seen[current]) {
        ctx->seen[current] = true; ctx->order[length++] = current / 2; int next = -1;
        for (int i = 0; i < ctx->degree[current]; ++i) if (ctx->neighbors[current][i] != previous) { next = ctx->neighbors[current][i]; break; }
        if (next < 0) break; previous = current; current = next;
    }
    bool cycle = current == start && ctx->degree[start] == 2; ++ctx->component; int left = 0;
    for (int right = 0; right < (cycle ? 2 * length : length); ++right) {
        int cell = ctx->order[right % length];
        if (ctx->stamp[cell] == ctx->component && ctx->last[cell] + 1 > left) left = ctx->last[cell] + 1;
        if (right - length + 1 > left) left = right - length + 1;
        ctx->stamp[cell] = ctx->component; ctx->last[cell] = right;
        if (right - left + 1 > ctx->best) ctx->best = right - left + 1;
    }
}
static void connect(int (*neighbors)[2], unsigned char* degree, int a, int b) { neighbors[a][degree[a]++] = b; neighbors[b][degree[b]++] = a; }
int solution(int** grid, size_t grid_rows, size_t grid_cols) {
    int rows = (int)grid_rows, cols = (int)grid_cols, cells = rows * cols, size = 2 * cells;
    int (*neighbors)[2] = malloc((size_t)size * sizeof(*neighbors)); unsigned char* degree = calloc((size_t)size,sizeof(*degree)); bool* seen = calloc((size_t)size,sizeof(*seen));
    int* order = malloc((size_t)size * sizeof(*order)); int* last = malloc((size_t)cells * sizeof(*last)); int* stamp = calloc((size_t)cells,sizeof(*stamp));
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        int base = 2 * (r * cols + c); if (r + 1 < rows) connect(neighbors,degree,base + 1,base + 2 * cols);
        if (c + 1 < cols) connect(neighbors,degree,base + (grid[r][c] == 1),base + 2 + (grid[r][c + 1] == -1));
    }
    Context ctx = {neighbors,degree,seen,order,last,stamp,0,1};
    for (int node = 0; node < size; ++node) if (!seen[node] && degree[node] < 2) inspect(&ctx,node);
    for (int node = 0; node < size; ++node) if (!seen[node]) inspect(&ctx,node);
    int answer = ctx.best; free(neighbors); free(degree); free(seen); free(order); free(last); free(stamp);
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
// typedef struct { int (*neighbors)[2]; unsigned char* degree; bool* seen; int* order; int* last; int* stamp; int component; int best; } Context;  // 작은 삼각형별 최대 두 이웃 / 작은 삼각형의 연결 수 / 이미 경로에 넣은 삼각형 / 경로에서 만난 원래 칸 번호 / 원래 칸을 마지막으로 본 순서를 한 상태로 묶기
// static void inspect(Context* ctx, int start) {  // 경로를 따라가며 같은 원래 칸이 겹치지 않는 최장 구간 계산
//     int previous = -1, current = start, length = 0;  // 직전에 지난 삼각형 / 현재 작은 삼각형 / 이번 경로 길이 저장
//     while (!ctx->seen[current]) {  // 삼각형을 방문 표시하고 해당 원래 칸 번호를 경로에 추가
//         ctx->seen[current] = true; ctx->order[length++] = current / 2; int next = -1;  // 삼각형을 방문 표시하고 해당 원래 칸 번호를 경로에 추가
//         for (int i = 0; i < ctx->degree[current]; ++i) if (ctx->neighbors[current][i] != previous) { next = ctx->neighbors[current][i]; break; }  // 직전에 온 삼각형을 빼고 앞으로 이어지는 이웃 선택
//         if (next < 0) break; previous = current; current = next;  // 직전 칸을 제외한 다음 삼각형가 0보다 작으면 이번 후보 확인을 끝내기
//     }  // 이 범위 끝
//     bool cycle = current == start && ctx->degree[start] == 2; ++ctx->component; int left = 0;  // 시작점으로 돌아오는 경로인지 여부 / 같은 칸이 중복되지 않는 구간 시작 저장
//     for (int right = 0; right < (cycle ? 2 * length : length); ++right) {  // 경로에서 확장할 위치 순서대로 확인
//         int cell = ctx->order[right % length];  // 현재 삼각형의 원래 칸 저장
//         if (ctx->stamp[cell] == ctx->component && ctx->last[cell] + 1 > left) left = ctx->last[cell] + 1;  // 같은 원래 칸이 구간 안에 다시 나오면 앞쪽 중복을 제외하도록 왼끝 이동
//         if (right - length + 1 > left) left = right - length + 1;  // 원형 경로를 한 바퀴 넘게 잡지 않도록 왼끝 제한
//         ctx->stamp[cell] = ctx->component; ctx->last[cell] = right;  // last가 속한 연결 성분 표시 / 원래 칸을 마지막으로 본 순서 갱신
//         if (right - left + 1 > ctx->best) ctx->best = right - left + 1;  // 같은 칸이 겹치지 않는 현재 구간이 더 길면 최장 길이 갱신
//     }  // 이 범위 끝
// }  // 이 범위 끝
// static void connect(int (*neighbors)[2], unsigned char* degree, int a, int b) { neighbors[a][degree[a]++] = b; neighbors[b][degree[b]++] = a; }  // 두 삼각형을 양방향으로 연결
// int solution(int** grid, size_t grid_rows, size_t grid_cols) {  // 삼각형은 두 바깥 변으로만 연결되어 이웃이 최대 2개; 따라서 전체 그래프는 경로 또는 고리로 나뉨
//     int rows = (int)grid_rows, cols = (int)grid_cols, cells = rows * cols, size = 2 * cells;  // 원래 격자 칸 수 / 작은 삼각형 전체 수 저장
//     int (*neighbors)[2] = malloc((size_t)size * sizeof(*neighbors)); unsigned char* degree = calloc((size_t)size,sizeof(*degree)); bool* seen = calloc((size_t)size,sizeof(*seen));  // 작은 삼각형의 연결 수 / 이미 경로에 넣은 삼각형 공간 확보하고 0으로 시작
//     int* order = malloc((size_t)size * sizeof(*order)); int* last = malloc((size_t)cells * sizeof(*last)); int* stamp = calloc((size_t)cells,sizeof(*stamp));  // 경로에서 만난 원래 칸 번호 / 원래 칸을 마지막으로 본 순서 / last가 속한 연결 성분 표시 공간 확보하고 0으로 시작
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 격자 행 순서대로 확인; 격자 열 갱신
//         int base = 2 * (r * cols + c); if (r + 1 < rows) connect(neighbors,degree,base + 1,base + 2 * cols);  // 원래 칸의 첫 삼각형 번호 저장
//         if (c + 1 < cols) connect(neighbors,degree,base + (grid[r][c] == 1),base + 2 + (grid[r][c + 1] == -1));  // 오른쪽 칸이 있으면 맞닿은 두 삼각형을 양방향으로 연결
//     }  // 이 범위 끝
//     Context ctx = {neighbors,degree,seen,order,last,stamp,0,1};  // 경로 탐색과 중복 구간 정보 저장
//     for (int node = 0; node < size; ++node) if (!seen[node] && degree[node] < 2) inspect(&ctx,node);  // 미방문 삼각형 중 차수가 2 미만인 끝점부터 열린 경로 탐색
//     for (int node = 0; node < size; ++node) if (!seen[node]) inspect(&ctx,node);  // 끝점 탐색 뒤 남은 미방문 삼각형은 닫힌 순환 경로로 탐색
//     int answer = ctx.best; free(neighbors); free(degree); free(seen); free(order); free(last); free(stamp);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 원래 칸 중복 없는 가장 긴 덩어리 반환
// }  // 이 범위 끝

// 풀이 요약
// 삼각형은 두 바깥 변으로만 연결되어 이웃이 최대 2개; 따라서 전체 그래프는 경로 또는 고리로 나뉨
// 덩어리는 그 위의 연속 구간이며, 같은 정사각형의 삼각형 두 개를 함께 고를 수 없으므로 중복 칸 없는 최장 구간을 찾기
// 예: [[1]]은 넓이 1; 고리는 두 번 이어 경계를 넘는 구간도 확인; 시간·공간 O(N*M)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_389629_%EA%B0%80%EC%9E%A5_%ED%81%B0_%EC%82%BC%EA%B0%81%ED%98%95_%EB%8D%A9%EC%96%B4%EB%A6%AC/README.md)
