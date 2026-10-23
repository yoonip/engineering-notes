# 발전소 회로 복구

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468375) · Level 3 · C

## 풀이

각 층의 구조가 같으므로 패널 위치에서 평면 BFS를 수행하고, 다른 층 사이는 엘리베이터 왕복 거리와 층 차이를 더하기
이후 (켜진 패널 집합, 현재 패널)의 비트마스크 DP로 선행 조건을 만족하는 다음 패널을 선택; 시간 O(KNM+K²2^K), 공간 O(KNM+K2^K)
예: 1번 패널의 선행 조건이 4번이면 출발 위치에 있어도 켜지 않음; 4번을 먼저 방문한 후 돌아와 켤 수 있음

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int k; int* travel; unsigned* required; int* memo; unsigned full; } Context;
static int search(Context* ctx, unsigned mask, int current) {
    if (mask == ctx->full) return 0;
    size_t index = (size_t)mask * ctx->k + current; if (ctx->memo[index] >= 0) return ctx->memo[index];
    int answer = 1000000000;
    for (int target = 0; target < ctx->k; ++target) {
        unsigned bit = 1u << target; if ((mask & bit) || (ctx->required[target] & mask) != ctx->required[target]) continue;
        int cost = ctx->travel[current * ctx->k + target] + search(ctx,mask | bit,target); if (cost < answer) answer = cost;
    }
    return ctx->memo[index] = answer;
}
int solution(int h, const char* grid[], size_t grid_len, int** panels, size_t panels_rows, size_t panels_cols, int** seqs, size_t seqs_rows, size_t seqs_cols) {
    (void)h; (void)panels_cols; (void)seqs_cols; int rows = (int)grid_len, cols = (int)strlen(grid[0]), size = rows * cols, k = (int)panels_rows, elevator = 0;
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (grid[r][c] == '@') elevator = r * cols + c;
    int* positions = malloc((size_t)k * sizeof(*positions)); int* maps = malloc((size_t)k * size * sizeof(*maps)); int* queue = malloc((size_t)size * sizeof(*queue));
    const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int i = 0; i < k; ++i) positions[i] = (panels[i][1] - 1) * cols + panels[i][2] - 1;
    for (int i = 0; i < k; ++i) {
        int* distance = maps + i * size; for (int at = 0; at < size; ++at) distance[at] = 1000000000;
        int first = 0, last = 0; queue[last++] = positions[i]; distance[positions[i]] = 0;
        while (first < last) {
            int at = queue[first++], r = at / cols, c = at % cols;
            for (int d = 0; d < 4; ++d) { int nr = r + dr[d], nc = c + dc[d]; if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != '#' && distance[nr * cols + nc] == 1000000000) { distance[nr * cols + nc] = distance[at] + 1; queue[last++] = nr * cols + nc; } }
        }
    }
    int* travel = malloc((size_t)k * k * sizeof(*travel)); unsigned* required = calloc((size_t)k,sizeof(*required));
    for (int i = 0; i < k; ++i) for (int j = 0; j < k; ++j) travel[i * k + j] = panels[i][0] == panels[j][0] ? maps[i * size + positions[j]] : maps[i * size + elevator] + abs(panels[i][0] - panels[j][0]) + maps[j * size + elevator];
    for (size_t i = 0; i < seqs_rows; ++i) required[seqs[i][1] - 1] |= 1u << (seqs[i][0] - 1);
    size_t states = ((size_t)1 << k) * k; int* memo = malloc(states * sizeof(*memo)); for (size_t i = 0; i < states; ++i) memo[i] = -1;
    Context ctx = {k,travel,required,memo,(1u << k) - 1}; int answer = search(&ctx,required[0] ? 0 : 1,0);
    free(positions); free(maps); free(queue); free(travel); free(required); free(memo);
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
// typedef struct { int k; int* travel; unsigned* required; int* memo; unsigned full; } Context;  // 전체 패널 수 / 패널 사이 이동 거리 / 패널별 선행 복구 비트 / 방문 집합과 현재 패널별 최소 남은 거리 / 전체 패널 방문 비트를 한 상태로 묶기
// static int search(Context* ctx, unsigned mask, int current) {  // 방문한 패널 집합과 현재 패널에서 남은 최소 복구 거리 탐색
//     if (mask == ctx->full) return 0;  // 모든 패널을 선택했으면 남은 이동 비용은 0
//     size_t index = (size_t)mask * ctx->k + current; if (ctx->memo[index] >= 0) return ctx->memo[index];  // 현재 방문 상태의 최소 남은 거리를 메모하고 반환
//     int answer = 1000000000;  // 선행 조건을 지킨 최소 이동 거리 저장
//     for (int target = 0; target < ctx->k; ++target) {  // 다음에 복구할 패널 순서대로 확인
//         unsigned bit = 1u << target; if ((mask & bit) || (ctx->required[target] & mask) != ctx->required[target]) continue;  // 이미 복구했거나 선행 패널을 다 복구하지 못한 후보는 건너뛰기
//         int cost = ctx->travel[current * ctx->k + target] + search(ctx,mask | bit,target); if (cost < answer) answer = cost;  // 다음 패널까지 거리와 남은 복구 최솟값을 더해 최소 비용 선택
//     }  // 이 범위 끝
//     return ctx->memo[index] = answer;  // 현재 방문 상태의 최소 남은 거리를 메모하고 반환
// }  // 이 범위 끝
// int solution(int h, const char* grid[], size_t grid_len, int** panels, size_t panels_rows, size_t panels_cols, int** seqs, size_t seqs_rows, size_t seqs_cols) {  // 각 층의 구조가 같으므로 패널 위치에서 평면 BFS를 수행하고, 다른 층 사이는 엘리베이터 왕복 거리와 층 차이를 더하기
//     (void)h; (void)panels_cols; (void)seqs_cols; int rows = (int)grid_len, cols = (int)strlen(grid[0]), size = rows * cols, k = (int)panels_rows, elevator = 0;  // 지도 행·열 수, 칸 수, 패널 수를 구하고 엘리베이터 위치 초기화
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (grid[r][c] == '@') elevator = r * cols + c;  // 지도에서 @ 문자의 엘리베이터 위치 찾기
//     int* positions = malloc((size_t)k * sizeof(*positions)); int* maps = malloc((size_t)k * size * sizeof(*maps)); int* queue = malloc((size_t)size * sizeof(*queue));  // 패널별 층 안 위치 / 각 패널에서 지도 칸까지의 거리 / 지도 BFS 대기 칸 공간 확보
//     const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 지도 BFS에서 쓸 상하좌우 행·열 변화량
//     for (int i = 0; i < k; ++i) positions[i] = (panels[i][1] - 1) * cols + panels[i][2] - 1;  // 출발 패널 순서대로 확인; 패널별 층 안 위치 갱신
//     for (int i = 0; i < k; ++i) {  // 출발 패널 순서대로 확인
//         int* distance = maps + i * size; for (int at = 0; at < size; ++at) distance[at] = 1000000000;  // 현재 패널의 거리 배열을 고르고 모든 칸을 미도달 값으로 초기화
//         int first = 0, last = 0; queue[last++] = positions[i]; distance[positions[i]] = 0;  // 현재 패널을 거리 0의 시작점으로 BFS 큐에 추가
//         while (first < last) {  // 큐에 미처리 정점이 남아 있는 동안 너비 우선 탐색을 계속하기
//             int at = queue[first++], r = at / cols, c = at % cols;  // 큐에서 현재 칸을 꺼내 행·열 좌표로 변환
//             for (int d = 0; d < 4; ++d) { int nr = r + dr[d], nc = c + dc[d]; if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] != '#' && distance[nr * cols + nc] == 1000000000) { distance[nr * cols + nc] = distance[at] + 1; queue[last++] = nr * cols + nc; } }  // 격자 안의 벽이 아닌 미방문 이웃에 거리 1을 더해 큐에 추가
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     int* travel = malloc((size_t)k * k * sizeof(*travel)); unsigned* required = calloc((size_t)k,sizeof(*required));  // 패널 사이 이동 거리 / 패널별 선행 복구 비트 공간 확보하고 0으로 시작
//     for (int i = 0; i < k; ++i) for (int j = 0; j < k; ++j) travel[i * k + j] = panels[i][0] == panels[j][0] ? maps[i * size + positions[j]] : maps[i * size + elevator] + abs(panels[i][0] - panels[j][0]) + maps[j * size + elevator];  // 같은 층은 직접 거리, 다른 층은 엘리베이터 접근 거리와 층 차이 사용
//     for (size_t i = 0; i < seqs_rows; ++i) required[seqs[i][1] - 1] |= 1u << (seqs[i][0] - 1);  // 각 패널보다 먼저 복구해야 하는 패널을 비트로 표시
//     size_t states = ((size_t)1 << k) * k; int* memo = malloc(states * sizeof(*memo)); for (size_t i = 0; i < states; ++i) memo[i] = -1;  // 패널 순서 DP의 상태 수 / 방문 집합과 현재 패널별 최소 남은 거리 / 출발 패널 공간 확보
//     Context ctx = {k,travel,required,memo,(1u << k) - 1}; int answer = search(&ctx,required[0] ? 0 : 1,0);  // 첫 패널의 선행 조건을 반영해 전체 복구 순서의 최소 거리 탐색
//     free(positions); free(maps); free(queue); free(travel); free(required); free(memo);  // 패널별 층 안 위치 / 각 패널에서 지도 칸까지의 거리 / 지도 BFS 대기 칸 / 패널 사이 이동 거리 임시 공간 정리
//     return answer;  // 선행 조건을 지킨 최소 이동 거리 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 층의 구조가 같으므로 패널 위치에서 평면 BFS를 수행하고, 다른 층 사이는 엘리베이터 왕복 거리와 층 차이를 더하기
// 이후 (켜진 패널 집합, 현재 패널)의 비트마스크 DP로 선행 조건을 만족하는 다음 패널을 선택; 시간 O(KNM+K²2^K), 공간 O(KNM+K2^K)
// 예: 1번 패널의 선행 조건이 4번이면 출발 위치에 있어도 켜지 않음; 4번을 먼저 방문한 후 돌아와 켤 수 있음
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:24:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/005_468375_%EB%B0%9C%EC%A0%84%EC%86%8C_%ED%9A%8C%EB%A1%9C_%EB%B3%B5%EA%B5%AC/README.md)
