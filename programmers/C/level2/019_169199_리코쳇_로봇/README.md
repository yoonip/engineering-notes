# 리코쳇 로봇

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/169199) · Level 2 · C

## 풀이

멈출 수 있는 위치를 정점으로 보고 한 번 미끄러지는 이동을 간선으로 삼아 너비 우선 탐색
예: 첫 게임판은 7번, 둘째는 목표에서 멈출 수 없어 -1.; 시간 O(행*열*max(행,열)), 공간 O(행*열)

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

int solution(const char* board[], size_t board_len) {
    int rows = (int)board_len, cols = (int)strlen(board[0]), answer = -1;
    int* distance = malloc((size_t)rows * cols * sizeof(*distance)); int* queue = malloc((size_t)rows * cols * sizeof(*queue));
    for (int i = 0; i < rows * cols; ++i) distance[i] = -1;
    int head = 0, tail = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (board[r][c] == 'R') { queue[tail++] = r * cols + c; distance[r * cols + c] = 0; }
    while (head < tail) {
        int at = queue[head++], r = at / cols, c = at % cols;
        if (board[r][c] == 'G') { answer = distance[at]; break; }
        for (int d = 0; d < 4; ++d) {
            int nr = r, nc = c;
            while (nr + dr[d] >= 0 && nr + dr[d] < rows && nc + dc[d] >= 0 && nc + dc[d] < cols && board[nr + dr[d]][nc + dc[d]] != 'D') { nr += dr[d]; nc += dc[d]; }
            if (distance[nr * cols + nc] == -1) { distance[nr * cols + nc] = distance[at] + 1; queue[tail++] = nr * cols + nc; }
        }
    }
    free(distance); free(queue);
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
// int solution(const char* board[], size_t board_len) {  // 멈출 수 있는 위치를 정점으로 보고 한 번 미끄러지는 이동을 간선으로 삼아 너비 우선 탐색
//     int rows = (int)board_len, cols = (int)strlen(board[0]), answer = -1;  // 보드 행 수 / 보드 열 수 / 목표까지의 최소 이동 횟수 저장
//     int* distance = malloc((size_t)rows * cols * sizeof(*distance)); int* queue = malloc((size_t)rows * cols * sizeof(*queue));  // 각 정지 칸까지의 최소 이동 수 / 다음으로 미끄러질 정지 칸 공간 확보
//     for (int i = 0; i < rows * cols; ++i) distance[i] = -1;  // 거리 초기화 위치 순서대로 확인; 각 정지 칸까지의 최소 이동 수 갱신
//     int head = 0, tail = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 큐에서 읽을 위치 / 큐에 넣을 위치 / 행 방향 변화 / 열 방향 변화 저장
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (board[r][c] == 'R') { queue[tail++] = r * cols + c; distance[r * cols + c] = 0; }  // 현재 행 순서대로 확인; 현재 열 / 큐에 넣을 위치 갱신
//     while (head < tail) {  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//         int at = queue[head++], r = at / cols, c = at % cols;  // 현재 정지 위치 / 현재 행 / 현재 열 저장
//         if (board[r][c] == 'G') { answer = distance[at]; break; }  // 목표 G에 도착했으면 현재 이동 횟수를 답으로 기록하고 종료
//         for (int d = 0; d < 4; ++d) {  // 이동 방향 번호 순서대로 확인
//             int nr = r, nc = c;  // 끝까지 미끄러진 행 / 끝까지 미끄러진 열 저장
//             while (nr + dr[d] >= 0 && nr + dr[d] < rows && nc + dc[d] >= 0 && nc + dc[d] < cols && board[nr + dr[d]][nc + dc[d]] != 'D') { nr += dr[d]; nc += dc[d]; }  // 다음 칸이 보드 안이고 장애물이 아니면 같은 방향으로 계속 미끄러지기
//             if (distance[nr * cols + nc] == -1) { distance[nr * cols + nc] = distance[at] + 1; queue[tail++] = nr * cols + nc; }  // 처음 도착한 정지 칸이면 이동 횟수 1을 더해 기록하고 큐에 추가
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(distance); free(queue);  // 각 정지 칸까지의 최소 이동 수 / 다음으로 미끄러질 정지 칸 임시 공간 정리
//     return answer;  // 목표까지의 최소 이동 횟수 반환
// }  // 이 범위 끝

// 풀이 요약
// 멈출 수 있는 위치를 정점으로 보고 한 번 미끄러지는 이동을 간선으로 삼아 너비 우선 탐색
// 예: 첫 게임판은 7번, 둘째는 목표에서 멈출 수 없어 -1.; 시간 O(행*열*max(행,열)), 공간 O(행*열)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:11:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/019_169199_%EB%A6%AC%EC%BD%94%EC%B3%87_%EB%A1%9C%EB%B4%87/README.md)
