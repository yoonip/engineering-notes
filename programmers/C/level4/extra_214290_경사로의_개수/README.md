# 경사로의 개수

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/214290) · Level 4 · C

## 풀이

수열 d 한 번의 출발·도착별 경로 수를 DP로 계산하고, 그 전이 행렬의 k제곱을 빠른 거듭제곱으로 적용하기
예: A→B가 2가지, B→C가 3가지라면 이어지는 경로는 6가지; 재방문을 허용하므로 행렬 곱으로 연결 가능
V=n*m, L=len(d).; 시간 O(L*V^2+V^3*log k), 공간 O(V^2)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static const int MOD = 1000000007;
static int* multiply(const int* a, const int* b, int size) {
    int* result = calloc((size_t)size * size,sizeof(*result));
    for (int i = 0; i < size; ++i) for (int mid = 0; mid < size; ++mid) if (a[i * size + mid]) for (int j = 0; j < size; ++j) result[i * size + j] = (int)((result[i * size + j] + (long long)a[i * size + mid] * b[mid * size + j]) % MOD);
    return result;
}
int solution(int** grid, size_t grid_rows, size_t grid_cols, int d[], size_t d_len, int k) {
    int rows = (int)grid_rows, cols = (int)grid_cols, size = rows * cols; int* matrix = calloc((size_t)size * size,sizeof(*matrix)); int* ways = malloc((size_t)size * sizeof(*ways)); int* next = malloc((size_t)size * sizeof(*next));
    const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int start = 0; start < size; ++start) {
        memset(ways,0,(size_t)size * sizeof(*ways)); ways[start] = 1;
        for (size_t step = 0; step < d_len; ++step) {
            memset(next,0,(size_t)size * sizeof(*next));
            for (int at = 0; at < size; ++at) if (ways[at]) {
                int r = at / cols, c = at % cols;
                for (int direction = 0; direction < 4; ++direction) { int nr = r + dr[direction], nc = c + dc[direction]; if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] - grid[r][c] == d[step]) next[nr * cols + nc] = (next[nr * cols + nc] + ways[at]) % MOD; }
            }
            int* temp = ways; ways = next; next = temp;
        }
        memcpy(matrix + start * size,ways,(size_t)size * sizeof(*ways));
    }
    for (int i = 0; i < size; ++i) ways[i] = 1;
    while (k) {
        if (k & 1) { memset(next,0,(size_t)size * sizeof(*next)); for (int i = 0; i < size; ++i) for (int j = 0; j < size; ++j) next[j] = (int)((next[j] + (long long)ways[i] * matrix[i * size + j]) % MOD); int* temp = ways; ways = next; next = temp; }
        k >>= 1; if (k) { int* squared = multiply(matrix,matrix,size); free(matrix); matrix = squared; }
    }
    long long answer = 0; for (int i = 0; i < size; ++i) answer += ways[i]; free(matrix); free(ways); free(next);
    return (int)(answer % MOD);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// static const int MOD = 1000000007;  // 경로 수 계산의 나머지 기준 1000000007
// static int* multiply(const int* a, const int* b, int size) {  // 시작·도착 사이의 경로 수 행렬 곱
//     int* result = calloc((size_t)size * size,sizeof(*result));  // 행렬 곱의 경로 수 공간 확보하고 0으로 시작
//     for (int i = 0; i < size; ++i) for (int mid = 0; mid < size; ++mid) if (a[i * size + mid]) for (int j = 0; j < size; ++j) result[i * size + j] = (int)((result[i * size + j] + (long long)a[i * size + mid] * b[mid * size + j]) % MOD);  // 중간 칸을 거치는 경로 수의 곱을 더해 전이 행렬 곱 계산
//     return result;  // 행렬 곱의 경로 수 반환
// }  // 이 범위 끝
// int solution(int** grid, size_t grid_rows, size_t grid_cols, int d[], size_t d_len, int k) {  // 수열 d 한 번의 출발·도착별 경로 수를 DP로 계산하고, 그 전이 행렬의 k제곱을 빠른 거듭제곱으로 적용하기
//     int rows = (int)grid_rows, cols = (int)grid_cols, size = rows * cols; int* matrix = calloc((size_t)size * size,sizeof(*matrix)); int* ways = malloc((size_t)size * sizeof(*ways)); int* next = malloc((size_t)size * sizeof(*next));  // 격자 행 수 / 격자 열 수 / 전체 칸 수 / 경사 수열 한 번의 시작 끝별 경로 수 공간 확보하고 0으로 시작
//     const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 행 이동 / 열 이동 저장
//     for (int start = 0; start < size; ++start) {  // 한 번의 경로를 시작할 칸 순서대로 확인
//         memset(ways,0,(size_t)size * sizeof(*ways)); ways[start] = 1;  // 현재 출발점에만 경우의 수 1을 놓고 나머지 칸은 0으로 초기화
//         for (size_t step = 0; step < d_len; ++step) {  // 적용할 경사 번호 순서대로 확인
//             memset(next,0,(size_t)size * sizeof(*next));  // 다음 경사 또는 제곱 단계의 방법 수 / 전체 칸 수 초기화
//             for (int at = 0; at < size; ++at) if (ways[at]) {  // 현재 단계에서 도달하는 경우의 수가 있는 칸만 다음 이동으로 확장
//                 int r = at / cols, c = at % cols;  // 현재 행 / 현재 열 저장
//                 for (int direction = 0; direction < 4; ++direction) { int nr = r + dr[direction], nc = c + dc[direction]; if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] - grid[r][c] == d[step]) next[nr * cols + nc] = (next[nr * cols + nc] + ways[at]) % MOD; }  // 상하좌우 중 높이 차가 다음 경사와 같은 칸에 경로 수 누적
//             }  // 이 범위 끝
//             int* temp = ways; ways = next; next = temp;  // 경로 수 배열 교환용 포인터 / 현재 단계에서 칸별 도달 방법 수 / 다음 경사 또는 제곱 단계의 방법 수 저장
//         }  // 이 범위 끝
//         memcpy(matrix + start * size,ways,(size_t)size * sizeof(*ways));  // 경사 수열 한 번의 시작 끝별 경로 수 / 한 번의 경로를 시작할 칸 / 전체 칸 수 복사
//     }  // 이 범위 끝
//     for (int i = 0; i < size; ++i) ways[i] = 1;  // 행렬 시작 칸 순서대로 확인; 현재 단계에서 칸별 도달 방법 수 갱신
//     while (k) {  // 남은 지수의 비트를 하나씩 처리하는 빠른 거듭제곱
//         if (k & 1) { memset(next,0,(size_t)size * sizeof(*next)); for (int i = 0; i < size; ++i) for (int j = 0; j < size; ++j) next[j] = (int)((next[j] + (long long)ways[i] * matrix[i * size + j]) % MOD); int* temp = ways; ways = next; next = temp; }  // 현재 지수 비트가 1이면 경로 수 벡터에 현재 전이 행렬 적용
//         k >>= 1; if (k) { int* squared = multiply(matrix,matrix,size); free(matrix); matrix = squared; }  // 지수 한 비트를 처리한 뒤 전이 행렬을 제곱하고 이전 행렬 해제
//     }  // 이 범위 끝
//     long long answer = 0; for (int i = 0; i < size; ++i) answer += ways[i]; free(matrix); free(ways); free(next);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return (int)(answer % MOD);  // 경사 수열을 k번 적용한 전체 경로 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 수열 d 한 번의 출발·도착별 경로 수를 DP로 계산하고, 그 전이 행렬의 k제곱을 빠른 거듭제곱으로 적용하기
// 예: A→B가 2가지, B→C가 3가지라면 이어지는 경로는 6가지; 재방문을 허용하므로 행렬 곱으로 연결 가능
// V=n*m, L=len(d).; 시간 O(L*V^2+V^3*log k), 공간 O(V^2)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_214290_%EA%B2%BD%EC%82%AC%EB%A1%9C%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
