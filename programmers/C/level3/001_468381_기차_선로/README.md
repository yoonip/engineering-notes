# 기차 선로

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468381) · Level 3 · C

## 풀이

기차가 실제로 움직이는 경로를 DFS로 만들기; 빈칸의 직선은 나중에 다른 축으로 다시 지날 때 교차 선로로 확정하기

기존 선로는 모두 지나야 하며, 기존 3번 선로는 두 축을 모두 사용해야 하기; 같은 방향 재방문은 순환이므로 중단하기

예: [[1,7],[0,2]]는 오른쪽으로 간 뒤 아래로 도착하는 기존 경로 한 가지; 빈칸은 그대로 두므로 답 1

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int size, cols; const int* original; int* rails; int* visited; int (*neighbors)[4]; } Context;
static int search(Context* ctx, int pos, int direction, unsigned remaining, unsigned pending) {
    static const unsigned ends[8] = {0,5,10,15,12,9,3,6};
    if (pos < 0 || ctx->original[pos] == -1) return 0;
    int axis = 1 << (direction % 2), kind = ctx->rails[pos], used = ctx->visited[pos];
    if (used) {
        if ((used & axis) || (kind != 1 && kind != 2 && kind != 3) || (kind != 3 && ctx->original[pos] != 0)) return 0;
        ctx->rails[pos] = 3; ctx->visited[pos] = 3;
        int result = search(ctx,ctx->neighbors[pos][direction],direction,remaining,pending & ~(1u << pos));
        ctx->rails[pos] = kind; ctx->visited[pos] = used; return result;
    }
    remaining &= ~(1u << pos);
    if (pos == ctx->size - 1) return ((kind == 1 && direction == 0) || (kind == 2 && direction == 1)) && !remaining && !pending;
    ctx->visited[pos] = axis; int result = 0;
    if (kind == 3) result = search(ctx,ctx->neighbors[pos][direction],direction,remaining,pending | (1u << pos));
    else {
        unsigned entry = 1u << ((direction + 2) % 4);
        for (int candidate = 1; candidate <= 7; ++candidate) {
            if (candidate == 3 || !(ends[candidate] & entry) || (kind && kind != candidate)) continue;
            unsigned exit = ends[candidate] ^ entry; int exit_direction = 0; while ((1u << exit_direction) != exit) ++exit_direction;
            ctx->rails[pos] = candidate; ctx->visited[pos] = candidate <= 2 ? axis : 3;
            result += search(ctx,ctx->neighbors[pos][exit_direction],exit_direction,remaining,pending);
        }
    }
    ctx->rails[pos] = kind; ctx->visited[pos] = 0;
    return result;
}
int solution(int** grid, size_t grid_rows, size_t grid_cols) {
    int size = (int)(grid_rows * grid_cols), cols = (int)grid_cols; int* original = malloc((size_t)size * sizeof(*original)); int* rails = malloc((size_t)size * sizeof(*rails)); int* visited = calloc((size_t)size, sizeof(*visited)); int (*neighbors)[4] = malloc((size_t)size * sizeof(*neighbors)); unsigned required = 0;
    for (int pos = 0; pos < size; ++pos) {
        int r = pos / cols, c = pos % cols; original[pos] = rails[pos] = grid[r][c]; if (original[pos] > 0) required |= 1u << pos;
        neighbors[pos][0] = c + 1 < cols ? pos + 1 : -1; neighbors[pos][1] = r + 1 < (int)grid_rows ? pos + cols : -1; neighbors[pos][2] = c ? pos - 1 : -1; neighbors[pos][3] = r ? pos - cols : -1;
    }
    visited[0] = 1; Context ctx = {size,cols,original,rails,visited,neighbors}; int answer = search(&ctx,1,0,required & ~1u,0);
    free(original); free(rails); free(visited); free(neighbors);
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
// typedef struct { int size, cols; const int* original; int* rails; int* visited; int (*neighbors)[4]; } Context;  // 전체 칸 수 / 격자 열 수 / 고정된 원래 선로 / 현재 탐색에서 놓은 선로 / 가로와 세로 통과 축을 한 상태로 묶기
// static int search(Context* ctx, int pos, int direction, unsigned remaining, unsigned pending) {  // 현재 칸·진입 방향·필수 선로·미완성 교차를 상태로 선로 배치 탐색
//     static const unsigned ends[8] = {0,5,10,15,12,9,3,6};  // 선로별 연결 방향 비트 저장
//     if (pos < 0 || ctx->original[pos] == -1) return 0;  // 격자 밖이거나 막힌 칸이면 이 경로는 실패
//     int axis = 1 << (direction % 2), kind = ctx->rails[pos], used = ctx->visited[pos];  // 가로·세로 중 이번 통과 축, 현재 선로, 이미 지난 축 읽기
//     if (used) {  // 이미 지난 칸이면 다른 축으로 교차 가능한지 확인
//         if ((used & axis) || (kind != 1 && kind != 2 && kind != 3) || (kind != 3 && ctx->original[pos] != 0)) return 0;  // 같은 축을 재사용했거나 허용되지 않는 칸 종류·회전이면 실패
//         ctx->rails[pos] = 3; ctx->visited[pos] = 3;  // 다른 축으로 다시 지나므로 이 칸을 교차 선로와 두 축 방문으로 표시
//         int result = search(ctx,ctx->neighbors[pos][direction],direction,remaining,pending & ~(1u << pos));  // 이번 선택을 반영한 상태를 다음 재귀 탐색에 전달하기
//         ctx->rails[pos] = kind; ctx->visited[pos] = used; return result;  // 재귀 결과를 보관하고 이 칸의 선로와 방문 축을 원래대로 복원
//     }  // 이 범위 끝
//     remaining &= ~(1u << pos);  // 처음 지난 필수 선로를 남은 비트에서 제거
//     if (pos == ctx->size - 1) return ((kind == 1 && direction == 0) || (kind == 2 && direction == 1)) && !remaining && !pending;  // 마지막 칸은 출구 방향과 칸 종류가 맞고 남은 조건이 모두 소진돼야 성공
//     ctx->visited[pos] = axis; int result = 0;  // 가로와 세로 통과 축 / 현재 분기에서 가능한 배치 수 갱신
//     if (kind == 3) result = search(ctx,ctx->neighbors[pos][direction],direction,remaining,pending | (1u << pos));  // 교차 선로는 직진하고 아직 다른 축을 지나야 하는 칸으로 표시
//     else {  // 교차 선로가 아니면 진입·출구가 맞는 후보 선로 시도
//         unsigned entry = 1u << ((direction + 2) % 4);  // 이동 방향의 반대편을 진입 연결점 비트로 만들기
//         for (int candidate = 1; candidate <= 7; ++candidate) {  // 이번 칸에 놓을 선로 후보 순서대로 확인
//             if (candidate == 3 || !(ends[candidate] & entry) || (kind && kind != candidate)) continue;  // 교차 선로이거나 진입 연결이 없거나 고정 선로와 다르면 후보 제외
//             unsigned exit = ends[candidate] ^ entry; int exit_direction = 0; while ((1u << exit_direction) != exit) ++exit_direction;  // 진입점을 뺀 나머지 연결점으로 출구 방향 찾기
//             ctx->rails[pos] = candidate; ctx->visited[pos] = candidate <= 2 ? axis : 3;  // 후보 선로를 놓고 직선은 현재 축, 꺾인 선로는 두 축 사용으로 표시
//             result += search(ctx,ctx->neighbors[pos][exit_direction],exit_direction,remaining,pending);  // 선택한 출구로 진행해서 가능한 완성 배치 수 더하기
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     ctx->rails[pos] = kind; ctx->visited[pos] = 0;  // 이 칸에 들어오기 전 선로와 미방문 상태로 되돌리기
//     return result;  // 현재 분기에서 가능한 배치 수 반환
// }  // 이 범위 끝
// int solution(int** grid, size_t grid_rows, size_t grid_cols) {  // 기차가 실제로 움직이는 경로를 DFS로 만들기; 빈칸의 직선은 나중에 다른 축으로 다시 지날 때 교차 선로로 확정하기
//     int size = (int)(grid_rows * grid_cols), cols = (int)grid_cols; int* original = malloc((size_t)size * sizeof(*original)); int* rails = malloc((size_t)size * sizeof(*rails)); int* visited = calloc((size_t)size, sizeof(*visited)); int (*neighbors)[4] = malloc((size_t)size * sizeof(*neighbors)); unsigned required = 0;  // 전체 칸 수 / 격자 열 수 / 고정된 원래 선로 / 현재 탐색에서 놓은 선로 공간 확보하고 0으로 시작
//     for (int pos = 0; pos < size; ++pos) {  // 현재 선로 칸 순서대로 확인
//         int r = pos / cols, c = pos % cols; original[pos] = rails[pos] = grid[r][c]; if (original[pos] > 0) required |= 1u << pos;  // 원래 칸 값을 복사하고 고정 선로가 있는 칸은 필수 방문 비트에 추가
//         neighbors[pos][0] = c + 1 < cols ? pos + 1 : -1; neighbors[pos][1] = r + 1 < (int)grid_rows ? pos + cols : -1; neighbors[pos][2] = c ? pos - 1 : -1; neighbors[pos][3] = r ? pos - cols : -1;  // 칸별 오른쪽 아래 왼쪽 위 이웃 갱신
//     }  // 이 범위 끝
//     visited[0] = 1; Context ctx = {size,cols,original,rails,visited,neighbors}; int answer = search(&ctx,1,0,required & ~1u,0);  // 시작 칸의 가로 통과를 표시한 뒤 오른쪽 칸부터 탐색
//     free(original); free(rails); free(visited); free(neighbors);  // 고정된 원래 선로 / 현재 탐색에서 놓은 선로 / 가로와 세로 통과 축 / 칸별 오른쪽 아래 왼쪽 위 이웃 임시 공간 정리
//     return answer;  // 필수 선로를 모두 지나는 완성 배치 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 기차가 실제로 움직이는 경로를 DFS로 만들기; 빈칸의 직선은 나중에 다른 축으로 다시 지날 때 교차 선로로 확정하기
// 기존 선로는 모두 지나야 하며, 기존 3번 선로는 두 축을 모두 사용해야 하기; 같은 방향 재방문은 순환이므로 중단하기
// 예: [[1,7],[0,2]]는 오른쪽으로 간 뒤 아래로 도착하는 기존 경로 한 가지; 빈칸은 그대로 두므로 답 1
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:05:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/001_468381_%EA%B8%B0%EC%B0%A8_%EC%84%A0%EB%A1%9C/README.md)
