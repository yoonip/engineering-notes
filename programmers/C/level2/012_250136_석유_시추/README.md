# [PCCP 기출문제] 2번 / 석유 시추

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250136) · Level 2 · C

## 풀이

연결된 석유를 큐로 탐색해 크기와 걸친 열 구하기; 덩어리 크기를 해당 열마다 한 번씩 더하기
예: 7번 열이 크기 7과 2 덩어리를 지나면 9.; 각 덩어리는 열마다 한 번만 더하기; 시간·공간 O(행*열)

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

int solution(int** land, size_t land_rows, size_t land_cols) {
    int rows = (int)land_rows, cols = (int)land_cols;
    bool* visited = calloc(land_rows * land_cols, sizeof(*visited)); int* queue = malloc(land_rows * land_cols * sizeof(*queue));
    int* totals = calloc(land_cols, sizeof(*totals)); const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        if (!land[r][c] || visited[r * cols + c]) continue;
        int head = 0, tail = 0, min_col = c, max_col = c; queue[tail++] = r * cols + c; visited[r * cols + c] = true;
        while (head < tail) {
            int at = queue[head++], x = at / cols, y = at % cols;
            if (y < min_col) min_col = y; if (y > max_col) max_col = y;
            for (int d = 0; d < 4; ++d) {
                int nx = x + dr[d], ny = y + dc[d];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && land[nx][ny] && !visited[nx * cols + ny]) {
                    visited[nx * cols + ny] = true; queue[tail++] = nx * cols + ny;
                }
            }
        }
        for (int col = min_col; col <= max_col; ++col) totals[col] += tail;
    }
    int answer = 0;
    for (int c = 0; c < cols; ++c) if (totals[c] > answer) answer = totals[c];
    free(visited); free(queue); free(totals);
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
// int solution(int** land, size_t land_rows, size_t land_cols) {  // 연결된 석유를 큐로 탐색해 크기와 걸친 열 구하기; 덩어리 크기를 해당 열마다 한 번씩 더하기
//     int rows = (int)land_rows, cols = (int)land_cols;  // 행 수 / 열 수 저장
//     bool* visited = calloc(land_rows * land_cols, sizeof(*visited)); int* queue = malloc(land_rows * land_cols * sizeof(*queue));  // 이미 확인한 석유 칸 / 현재 석유 덩어리의 칸 공간 확보하고 0으로 시작
//     int* totals = calloc(land_cols, sizeof(*totals)); const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 열별 시추 가능한 총석유량 / 행 이동 / 열 이동 공간 확보하고 0으로 시작
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 새 덩어리 행 순서대로 확인; 새 덩어리 열 갱신
//         if (!land[r][c] || visited[r * cols + c]) continue;  // 석유가 없거나 이미 같은 덩어리에 넣은 칸은 건너뛰기
//         int head = 0, tail = 0, min_col = c, max_col = c; queue[tail++] = r * cols + c; visited[r * cols + c] = true;  // 큐에서 읽을 위치 / 덩어리에 들어간 칸 수 / 덩어리가 차지한 가장 왼쪽 열 / 덩어리가 차지한 가장 오른쪽 열 / 현재 석유 덩어리의 칸 저장
//         while (head < tail) {  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//             int at = queue[head++], x = at / cols, y = at % cols;  // 현재 석유 칸 번호 / 현재 행 / 현재 열 저장
//             if (y < min_col) min_col = y; if (y > max_col) max_col = y;  // 석유 덩어리가 닿는 열의 최솟값과 최댓값 갱신
//             for (int d = 0; d < 4; ++d) {  // 이웃 방향 순서대로 확인
//                 int nx = x + dr[d], ny = y + dc[d];  // 다음 행 / 다음 열 저장
//                 if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && land[nx][ny] && !visited[nx * cols + ny]) {  // 격자 안의 아직 안 간 이동 가능한 칸이면 처리
//                     visited[nx * cols + ny] = true; queue[tail++] = nx * cols + ny;  // 이미 확인한 석유 칸 / 현재 석유 덩어리의 칸 갱신
//                 }  // 이 범위 끝
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         for (int col = min_col; col <= max_col; ++col) totals[col] += tail;  // 현재 덩어리에 걸친 열 순서대로 확인; 열별 시추 가능한 총석유량 / 현재 덩어리에 걸친 열 / 덩어리에 들어간 칸 수 더해 누적
//     }  // 이 범위 끝
//     int answer = 0;  // 한 열로 얻는 최대 석유량 저장
//     for (int c = 0; c < cols; ++c) if (totals[c] > answer) answer = totals[c];  // 열별로 모은 석유량 중 최댓값 선택
//     free(visited); free(queue); free(totals);  // 이미 확인한 석유 칸 / 현재 석유 덩어리의 칸 / 열별 시추 가능한 총석유량 임시 공간 정리
//     return answer;  // 한 열로 얻는 최대 석유량 반환
// }  // 이 범위 끝

// 풀이 요약
// 연결된 석유를 큐로 탐색해 크기와 걸친 열 구하기; 덩어리 크기를 해당 열마다 한 번씩 더하기
// 예: 7번 열이 크기 7과 2 덩어리를 지나면 9.; 각 덩어리는 열마다 한 번만 더하기; 시간·공간 O(행*열)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/012_250136_%EC%84%9D%EC%9C%A0_%EC%8B%9C%EC%B6%94/README.md)
