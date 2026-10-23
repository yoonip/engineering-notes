# 퍼즐 조각 채우기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/84021) · Level 3 · C

## 풀이

빈 공간과 조각을 큐로 추출하고 네 회전 중 가장 작은 좌표 키로 정규화; 같은 키의 아직 안 쓴 조각과 짝짓기
예: 4칸 빈 공간과 회전해서 같은 조각이 만나면 4칸 추가하고 사용 표시; 반사는 허용하지 않기
조각 크기는 최대 6; 빈 공간 H개·조각 P개이면 시간 O(N²+HP), 공간 O(N²); 각 공간은 같은 키의 조각 중 아무 하나와 연결 가능

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int row, col; } Cell;
typedef struct { uint64_t key; int size; bool used; } Shape;
static int compare_cell(const void* p, const void* q) { const Cell* a = p; const Cell* b = q; return a->row != b->row ? a->row - b->row : a->col - b->col; }
static uint64_t canonical(Cell* cells, int count) {
    uint64_t best = UINT64_MAX;
    for (int rotation = 0; rotation < 4; ++rotation) {
        Cell normalized[6]; int min_r = INT_MAX, min_c = INT_MAX;
        for (int i = 0; i < count; ++i) { if (cells[i].row < min_r) min_r = cells[i].row; if (cells[i].col < min_c) min_c = cells[i].col; }
        for (int i = 0; i < count; ++i) normalized[i] = (Cell){cells[i].row - min_r,cells[i].col - min_c};
        qsort(normalized, (size_t)count, sizeof(*normalized), compare_cell); uint64_t key = (uint64_t)count << 36;
        for (int i = 0; i < count; ++i) key |= (uint64_t)(normalized[i].row * 6 + normalized[i].col) << (6 * i);
        if (key < best) best = key;
        for (int i = 0; i < count; ++i) { int row = cells[i].row; cells[i].row = cells[i].col; cells[i].col = -row; }
    }
    return best;
}
static int collect(int** board, int n, int target, Shape* result) {
    bool* visited = calloc((size_t)n * n, sizeof(*visited)); int* queue = malloc((size_t)n * n * sizeof(*queue)); int count = 0;
    const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) {
        if (visited[r * n + c] || board[r][c] != target) continue;
        int head = 0, tail = 0; queue[tail++] = r * n + c; visited[r * n + c] = true; Cell cells[6];
        while (head < tail) {
            int at = queue[head], x = at / n, y = at % n; cells[head++] = (Cell){x,y};
            for (int d = 0; d < 4; ++d) { int nx = x + dr[d], ny = y + dc[d]; if (nx >= 0 && nx < n && ny >= 0 && ny < n && !visited[nx * n + ny] && board[nx][ny] == target) { visited[nx * n + ny] = true; queue[tail++] = nx * n + ny; } }
        }
        result[count++] = (Shape){canonical(cells,tail),tail,false};
    }
    free(visited); free(queue);
    return count;
}
int solution(int** game_board, size_t game_board_rows, size_t game_board_cols, int** table, size_t table_rows, size_t table_cols) {
    (void)game_board_cols; (void)table_rows; (void)table_cols; int n = (int)game_board_rows;
    Shape* holes = malloc((size_t)n * n * sizeof(*holes)); Shape* pieces = malloc((size_t)n * n * sizeof(*pieces));
    int h = collect(game_board,n,0,holes), p = collect(table,n,1,pieces), answer = 0;
    for (int i = 0; i < h; ++i) for (int j = 0; j < p; ++j) if (!pieces[j].used && holes[i].key == pieces[j].key) { pieces[j].used = true; answer += holes[i].size; break; }
    free(holes); free(pieces);
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
// typedef struct { int row, col; } Cell;  // 회전 전에 보관할 행를 한 상태로 묶기
// typedef struct { uint64_t key; int size; bool used; } Shape;  // 정렬한 좌표를 압축한 비트 키를 한 상태로 묶기
// static int compare_cell(const void* p, const void* q) { const Cell* a = p; const Cell* b = q; return a->row != b->row ? a->row - b->row : a->col - b->col; }  // 좌표를 행 우선, 열 다음 순서로 정렬
// static uint64_t canonical(Cell* cells, int count) {  // 네 회전을 비교해서 같은 조각의 정규 키 만들기
//     uint64_t best = UINT64_MAX;  // 네 회전 중 정규 모양 키 갱신
//     for (int rotation = 0; rotation < 4; ++rotation) {  // 90도 회전 횟수 순서대로 확인
//         Cell normalized[6]; int min_r = INT_MAX, min_c = INT_MAX;  // 회전 후 최소 행 / 회전 후 최소 열 저장
//         for (int i = 0; i < count; ++i) { if (cells[i].row < min_r) min_r = cells[i].row; if (cells[i].col < min_c) min_c = cells[i].col; }  // 채울 빈칸 조각 순서대로 확인; 회전 후 최소 행 / 회전 후 최소 열 갱신
//         for (int i = 0; i < count; ++i) normalized[i] = (Cell){cells[i].row - min_r,cells[i].col - min_c};  // 채울 빈칸 조각 순서대로 확인; 왼쪽 위로 당긴 조각 좌표 갱신
//         qsort(normalized, (size_t)count, sizeof(*normalized), compare_cell); uint64_t key = (uint64_t)count << 36;  // 왼쪽 위로 당긴 조각 좌표 / 조각의 칸 수 정렬 순서 맞추기
//         for (int i = 0; i < count; ++i) key |= (uint64_t)(normalized[i].row * 6 + normalized[i].col) << (6 * i);  // 채울 빈칸 조각 순서대로 확인; 정렬한 좌표를 압축한 비트 키 / 왼쪽 위로 당긴 조각 좌표 / 채울 빈칸 조각 비트 상태 갱신
//         if (key < best) best = key;  // 네 회전 중 가장 작은 키를 이 조각의 대표 모양으로 선택
//         for (int i = 0; i < count; ++i) { int row = cells[i].row; cells[i].row = cells[i].col; cells[i].col = -row; }  // 채울 빈칸 조각 순서대로 확인; 회전 전에 보관할 행 저장
//     }  // 이 범위 끝
//     return best;  // 네 회전 중 정규 모양 키 반환
// }  // 이 범위 끝
// static int collect(int** board, int n, int target, Shape* result) {  // 연결된 칸을 한 조각으로 묶어 정규 키 저장
//     bool* visited = calloc((size_t)n * n, sizeof(*visited)); int* queue = malloc((size_t)n * n * sizeof(*queue)); int count = 0;  // 이미 조각에 포함한 칸 / 연결 조각 탐색 큐 / 조각의 칸 수 공간 확보하고 0으로 시작
//     const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 행 변화 / 열 변화 저장
//     for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) {  // 새 조각 시작 행 순서대로 확인; 새 조각 시작 열 갱신
//         if (visited[r * n + c] || board[r][c] != target) continue;  // 이미 조각에 넣은 칸이나 찾는 값과 다른 칸은 건너뛰기
//         int head = 0, tail = 0; queue[tail++] = r * n + c; visited[r * n + c] = true; Cell cells[6];  // 조각 시작 칸을 방문 표시하고 BFS 큐와 최대 여섯 좌표 공간 준비
//         while (head < tail) {  // 큐에 미처리 정점이 남아 있는 동안 너비 우선 탐색을 계속하기
//             int at = queue[head], x = at / n, y = at % n; cells[head++] = (Cell){x,y};  // 큐에서 현재 칸을 꺼내 조각의 좌표 목록에 추가
//             for (int d = 0; d < 4; ++d) { int nx = x + dr[d], ny = y + dc[d]; if (nx >= 0 && nx < n && ny >= 0 && ny < n && !visited[nx * n + ny] && board[nx][ny] == target) { visited[nx * n + ny] = true; queue[tail++] = nx * n + ny; } }  // 이웃 방향 순서대로 확인; 이웃 행 / 이웃 열 / 이미 조각에 포함한 칸 / 연결 조각 탐색 큐 저장
//         }  // 이 범위 끝
//         result[count++] = (Shape){canonical(cells,tail),tail,false};  // 현재 조각의 정규 키와 칸 수, 미사용 표시 저장
//     }  // 이 범위 끝
//     free(visited); free(queue);  // 이미 조각에 포함한 칸 / 연결 조각 탐색 큐 임시 공간 정리
//     return count;  // 추출한 조각 개수 반환
// }  // 이 범위 끝
// int solution(int** game_board, size_t game_board_rows, size_t game_board_cols, int** table, size_t table_rows, size_t table_cols) {  // 빈 공간과 조각을 큐로 추출하고 네 회전 중 가장 작은 좌표 키로 정규화; 같은 키의 아직 안 쓴 조각과 짝짓기
//     (void)game_board_cols; (void)table_rows; (void)table_cols; int n = (int)game_board_rows;  // (void)game_board_cols; (void)table_rows; (void)table_cols; int n = (int)game_board_rows
//     Shape* holes = malloc((size_t)n * n * sizeof(*holes)); Shape* pieces = malloc((size_t)n * n * sizeof(*pieces));  // 보드 빈칸의 정규 모양 / 테이블 조각의 정규 모양 공간 확보
//     int h = collect(game_board,n,0,holes), p = collect(table,n,1,pieces), answer = 0;  // 빈칸 조각 수 / 테이블 조각 수 / 채운 전체 칸 수 저장
//     for (int i = 0; i < h; ++i) for (int j = 0; j < p; ++j) if (!pieces[j].used && holes[i].key == pieces[j].key) { pieces[j].used = true; answer += holes[i].size; break; }  // 채울 빈칸 조각 순서대로 확인; 맞춰 볼 테이블 조각 갱신
//     free(holes); free(pieces);  // 보드 빈칸의 정규 모양 / 테이블 조각의 정규 모양 임시 공간 정리
//     return answer;  // 채운 전체 칸 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 빈 공간과 조각을 큐로 추출하고 네 회전 중 가장 작은 좌표 키로 정규화; 같은 키의 아직 안 쓴 조각과 짝짓기
// 예: 4칸 빈 공간과 회전해서 같은 조각이 만나면 4칸 추가하고 사용 표시; 반사는 허용하지 않기
// 조각 크기는 최대 6; 빈 공간 H개·조각 P개이면 시간 O(N²+HP), 공간 O(N²); 각 공간은 같은 키의 조각 중 아무 하나와 연결 가능
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:33:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/038_84021_%ED%8D%BC%EC%A6%90_%EC%A1%B0%EA%B0%81_%EC%B1%84%EC%9A%B0%EA%B8%B0/README.md)
