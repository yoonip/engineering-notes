#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int* solution(int m, int n, int h, int w, int** drops, size_t drops_rows, size_t drops_cols) {
    (void)drops_cols;
    int never = (int)drops_rows + 1, cols = n - w + 1;
    int* rain = malloc((size_t)m * n * sizeof(*rain)); int* row_min = malloc((size_t)m * cols * sizeof(*row_min));
    int capacity = m > n ? m : n; int* queue = malloc((size_t)capacity * sizeof(*queue));
    for (int i = 0; i < m * n; ++i) rain[i] = never;
    for (size_t i = 0; i < drops_rows; ++i) rain[drops[i][0] * n + drops[i][1]] = (int)i + 1;
    for (int r = 0; r < m; ++r) {
        int head = 0, tail = 0;
        for (int c = 0; c < n; ++c) {
            while (head < tail && queue[head] <= c - w) ++head;
            while (head < tail && rain[r * n + queue[tail - 1]] >= rain[r * n + c]) --tail;
            queue[tail++] = c;
            if (c >= w - 1) row_min[r * cols + c - w + 1] = rain[r * n + queue[head]];
        }
    }
    int* answer = calloc(2, sizeof(*answer)); int best = -1;
    for (int c = 0; c < cols; ++c) {
        int head = 0, tail = 0;
        for (int r = 0; r < m; ++r) {
            while (head < tail && queue[head] <= r - h) ++head;
            while (head < tail && row_min[queue[tail - 1] * cols + c] >= row_min[r * cols + c]) --tail;
            queue[tail++] = r;
            if (r >= h - 1) {
                int top = r - h + 1, time = row_min[queue[head] * cols + c];
                if (time > best || (time == best && (top < answer[0] || (top == answer[0] && c < answer[1])))) { best = time; answer[0] = top; answer[1] = c; }
            }
        }
    }
    free(rain); free(row_min); free(queue);
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
// int* solution(int m, int n, int h, int w, int** drops, size_t drops_rows, size_t drops_cols) {  // 각 칸의 빗방울 시각을 기록하고, 가로·세로 단조 덱으로 직사각형의 첫 비 시각을 계산
//     (void)drops_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int never = (int)drops_rows + 1, cols = n - w + 1;  // 끝까지 비가 안 오는 칸의 시각 / 가로 구역을 놓을 수 있는 시작 열 수 저장
//     int* rain = malloc((size_t)m * n * sizeof(*rain)); int* row_min = malloc((size_t)m * cols * sizeof(*row_min));  // 각 칸에 비가 처음 오는 순서 / 가로 w칸에서 가장 빠른 빗방울 공간 확보
//     int capacity = m > n ? m : n; int* queue = malloc((size_t)capacity * sizeof(*queue));  // 긴 쪽 크기에 맞춘 큐 용량 / 최솟값 후보를 담는 단조 큐 공간 확보
//     for (int i = 0; i < m * n; ++i) rain[i] = never;  // 빗방울 또는 초기화 위치 순서대로 확인; 각 칸에 비가 처음 오는 순서 갱신
//     for (size_t i = 0; i < drops_rows; ++i) rain[drops[i][0] * n + drops[i][1]] = (int)i + 1;  // 빗방울 또는 초기화 위치 순서대로 확인; 각 칸에 비가 처음 오는 순서 / 빗방울 또는 초기화 위치 확인
//     for (int r = 0; r < m; ++r) {  // 검사할 행 순서대로 확인
//         int head = 0, tail = 0;  // 유효 후보의 맨 앞 / 후보 큐 다음 위치 저장
//         for (int c = 0; c < n; ++c) {  // 검사할 열 순서대로 확인
//             while (head < tail && queue[head] <= c - w) ++head;  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//             while (head < tail && rain[r * n + queue[tail - 1]] >= rain[r * n + c]) --tail;  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//             queue[tail++] = c;  // 최솟값 후보를 담는 단조 큐 갱신
//             if (c >= w - 1) row_min[r * cols + c - w + 1] = rain[r * n + queue[head]];  // 가로 w칸이 채워졌으면 단조 큐 맨 앞의 최소 빗방울 시각 기록
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     int* answer = calloc(2, sizeof(*answer)); int best = -1;  // 가장 늦게 젖는 구역의 왼쪽 위 좌표 / 지금까지 가장 늦은 첫 빗방울 공간 확보하고 0으로 시작
//     for (int c = 0; c < cols; ++c) {  // 검사할 열 순서대로 확인
//         int head = 0, tail = 0;  // 유효 후보의 맨 앞 / 후보 큐 다음 위치 저장
//         for (int r = 0; r < m; ++r) {  // 검사할 행 순서대로 확인
//             while (head < tail && queue[head] <= r - h) ++head;  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//             while (head < tail && row_min[queue[tail - 1] * cols + c] >= row_min[r * cols + c]) --tail;  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//             queue[tail++] = r;  // 최솟값 후보를 담는 단조 큐 갱신
//             if (r >= h - 1) {  // 세로 h칸이 채워졌으면 직사각형의 첫 빗방울 시각 비교
//                 int top = r - h + 1, time = row_min[queue[head] * cols + c];  // 세로 h칸 구역의 시작 행 / 현재 구역이 처음 젖는 시각 저장
//                 if (time > best || (time == best && (top < answer[0] || (top == answer[0] && c < answer[1])))) { best = time; answer[0] = top; answer[1] = c; }  // 더 늦게 젖는 구역을 선택하고 동률이면 위쪽, 왼쪽 순서로 선택
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(rain); free(row_min); free(queue);  // 각 칸에 비가 처음 오는 순서 / 가로 w칸에서 가장 빠른 빗방울 / 최솟값 후보를 담는 단조 큐 임시 공간 정리
//     return answer;  // 가장 늦게 젖는 구역의 왼쪽 위 좌표 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 칸의 빗방울 시각을 기록하고, 가로·세로 단조 덱으로 직사각형의 첫 비 시각을 계산
// 첫 비가 가장 늦는 좌표를 선택하고, 동률이면 위쪽·왼쪽을 우선하기; 시간·공간 O(m*n)
