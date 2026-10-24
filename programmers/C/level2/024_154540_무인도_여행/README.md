# 무인도 여행

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/154540) · Level 2 · C

## 풀이

상하좌우로 연결된 땅을 큐로 탐색하며 식량 합산; 별도 방문 배열로 같은 땅을 두 번 세지 않기

예: 섬의 합 27,1,1을 정렬해 [1,1,27]; 칸 수 V, 섬 수 K일 때 시간 O(V+K log K), 공간 O(V)

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

static int compare(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }
int* solution(const char* maps[], size_t maps_len) {
    int rows = (int)maps_len, cols = (int)strlen(maps[0]); size_t size = (size_t)rows * cols;
    bool* visited = calloc(size, sizeof(*visited)); int* queue = malloc(size * sizeof(*queue)); int* answer = malloc(size * sizeof(*answer));
    int count = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        if (visited[r * cols + c] || maps[r][c] == 'X') continue;
        size_t head = 0, tail = 0; queue[tail++] = r * cols + c; visited[r * cols + c] = true; int food = 0;
        while (head < tail) {
            int at = queue[head++], x = at / cols, y = at % cols; food += maps[x][y] - '0';
            for (int d = 0; d < 4; ++d) {
                int nx = x + dr[d], ny = y + dc[d];
                if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && !visited[nx * cols + ny] && maps[nx][ny] != 'X') {
                    visited[nx * cols + ny] = true; queue[tail++] = nx * cols + ny;
                }
            }
        }
        answer[count++] = food;
    }
    if (!count) answer[count++] = -1;
    qsort(answer, count, sizeof(*answer), compare); free(visited); free(queue);
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
// static int compare(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }  // 섬의 식량 합을 작은 값부터 정렬
// int* solution(const char* maps[], size_t maps_len) {  // 상하좌우로 연결된 땅을 큐로 탐색하며 식량 합산; 별도 방문 배열로 같은 땅을 두 번 세지 않기
//     int rows = (int)maps_len, cols = (int)strlen(maps[0]); size_t size = (size_t)rows * cols;  // 지도의 행 수 / 지도의 열 수 / 지도 전체 칸 수 저장
//     bool* visited = calloc(size, sizeof(*visited)); int* queue = malloc(size * sizeof(*queue)); int* answer = malloc(size * sizeof(*answer));  // 이미 같은 섬에 넣은 칸 / 현재 섬의 탐색 대기 칸 / 섬별 식량 합 공간 확보하고 0으로 시작
//     int count = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 발견한 섬 수 / 행 방향 변화 / 열 방향 변화 저장
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 섬을 시작할 행 순서대로 확인; 섬을 시작할 열 갱신
//         if (visited[r * cols + c] || maps[r][c] == 'X') continue;  // 이미 확인한 칸이나 바다는 새 섬 탐색에서 제외
//         size_t head = 0, tail = 0; queue[tail++] = r * cols + c; visited[r * cols + c] = true; int food = 0;  // 새 섬의 시작 칸을 방문 표시하고 큐와 식량 합 초기화
//         while (head < tail) {  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//             int at = queue[head++], x = at / cols, y = at % cols; food += maps[x][y] - '0';  // 현재 섬의 칸을 꺼내 식량 숫자 더하기
//             for (int d = 0; d < 4; ++d) {  // 이웃 방향 번호 순서대로 확인
//                 int nx = x + dr[d], ny = y + dc[d];  // 다음 행 / 다음 열 저장
//                 if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && !visited[nx * cols + ny] && maps[nx][ny] != 'X') {  // 격자 안의 아직 안 간 이동 가능한 칸이면 처리
//                     visited[nx * cols + ny] = true; queue[tail++] = nx * cols + ny;  // 이미 같은 섬에 넣은 칸 / 현재 섬의 탐색 대기 칸 갱신
//                 }  // 이 범위 끝
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         answer[count++] = food;  // 섬 하나의 식량 합을 결과에 추가
//     }  // 이 범위 끝
//     if (!count) answer[count++] = -1;  // 섬 하나의 식량 합을 결과에 추가
//     qsort(answer, count, sizeof(*answer), compare); free(visited); free(queue);  // 섬별 식량 합 / 발견한 섬 수 정렬 순서 맞추기
//     return answer;  // 섬별 식량 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 상하좌우로 연결된 땅을 큐로 탐색하며 식량 합산; 별도 방문 배열로 같은 땅을 두 번 세지 않기
// 예: 섬의 합 27,1,1을 정렬해 [1,1,27]; 칸 수 V, 섬 수 K일 때 시간 O(V+K log K), 공간 O(V)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/024_154540_%EB%AC%B4%EC%9D%B8%EB%8F%84_%EC%97%AC%ED%96%89/README.md)
