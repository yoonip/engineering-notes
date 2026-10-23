#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int compare(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }
int* solution(const char* grid[], size_t grid_len) {
    int rows = (int)grid_len, cols = (int)strlen(grid[0]);
    bool* visited = calloc((size_t)rows * cols * 4, sizeof(*visited));
    int* answer = malloc((size_t)rows * cols * 4 * sizeof(*answer));
    int count = 0; const int dr[4] = {-1,0,1,0}, dc[4] = {0,1,0,-1};
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) for (int direction = 0; direction < 4; ++direction) {
        int x = r, y = c, d = direction, length = 0;
        if (visited[(x * cols + y) * 4 + d]) continue;
        while (!visited[(x * cols + y) * 4 + d]) {
            visited[(x * cols + y) * 4 + d] = true; ++length;
            if (grid[x][y] == 'L') d = (d + 3) % 4;
            else if (grid[x][y] == 'R') d = (d + 1) % 4;
            x = (x + dr[d] + rows) % rows; y = (y + dc[d] + cols) % cols;
        }
        answer[count++] = length;
    }
    qsort(answer, count, sizeof(*answer), compare); free(visited);
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
// static int compare(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }  // 사이클 길이를 작은 값부터 정렬
// int* solution(const char* grid[], size_t grid_len) {  // (칸,진행 방향)을 상태로 탐색; 각 상태의 다음·이전 상태가 유일하므로 미방문 상태에서 출발하면 하나의 사이클을 얻기
//     int rows = (int)grid_len, cols = (int)strlen(grid[0]);  // 격자 행 수 / 격자 열 수 저장
//     bool* visited = calloc((size_t)rows * cols * 4, sizeof(*visited));  // 행 열 방향별 방문 여부 공간 확보하고 0으로 시작
//     int* answer = malloc((size_t)rows * cols * 4 * sizeof(*answer));  // 각 빛 경로의 사이클 길이 공간 확보
//     int count = 0; const int dr[4] = {-1,0,1,0}, dc[4] = {0,1,0,-1};  // 발견한 사이클 수 / 방향별 행 이동 / 방향별 열 이동 저장
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) for (int direction = 0; direction < 4; ++direction) {  // 시작 행 순서대로 확인; 시작 열 / 새 경로의 시작 방향 갱신
//         int x = r, y = c, d = direction, length = 0;  // 현재 광선 행 / 현재 광선 열 / 현재 진행 방향 / 이번 경로에서 지난 상태 수 저장
//         if (visited[(x * cols + y) * 4 + d]) continue;  // 이미 다른 사이클에서 확인한 행·열·방향 상태는 건너뛰기
//         while (!visited[(x * cols + y) * 4 + d]) {  // 같은 행·열·방향 상태를 다시 만날 때까지 광선 이동
//             visited[(x * cols + y) * 4 + d] = true; ++length;  // 행 열 방향별 방문 여부 갱신
//             if (grid[x][y] == 'L') d = (d + 3) % 4;  // L 칸이면 진행 방향을 왼쪽으로 90도 회전
//             else if (grid[x][y] == 'R') d = (d + 1) % 4;  // R 칸이면 진행 방향을 오른쪽으로 90도 회전
//             x = (x + dr[d] + rows) % rows; y = (y + dc[d] + cols) % cols;  // 현재 광선 행 / 현재 광선 열 갱신
//         }  // 이 범위 끝
//         answer[count++] = length;  // 각 빛 경로의 사이클 길이 갱신
//     }  // 이 범위 끝
//     qsort(answer, count, sizeof(*answer), compare); free(visited);  // 각 빛 경로의 사이클 길이 / 발견한 사이클 수 정렬 순서 맞추기
//     return answer;  // 각 빛 경로의 사이클 길이 반환
// }  // 이 범위 끝

// 풀이 요약
// (칸,진행 방향)을 상태로 탐색; 각 상태의 다음·이전 상태가 유일하므로 미방문 상태에서 출발하면 하나의 사이클을 얻기
// 예: ['SL','LR']은 16, ['S']는 길이 1 네 개.; 상태 수 V=4*행*열, 사이클 수 K일 때 시간 O(V+K log K), 공간 O(V)
