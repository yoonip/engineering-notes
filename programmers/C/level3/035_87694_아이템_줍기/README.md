# 아이템 줍기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/87694) · Level 3 · C

## 풀이

좌표를 두 배로 확대하고 직사각형들을 전부 채운 뒤, 각 직사각형의 내부를 모두 지워 합친 지형의 테두리를 만들기
테두리 위에서 BFS를 하면 최단 이동 거리; 좌표 확대 때문에 생긴 거리 두 배를 마지막에 나누기; 좌표 최대값 C에 대해 시간·공간 O(C²), 직사각형 수는 최대 4
예: 원래 한 칸 너비의 굴곡도 두 칸 간격으로 표현되어, 인접해 보이는 서로 다른 테두리를 가로지르는 지름길을 막기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int** rectangle, size_t rectangle_rows, size_t rectangle_cols, int characterX, int characterY, int itemX, int itemY) {
    (void)rectangle_cols; int board[102][102] = {{0}};
    for (size_t i = 0; i < rectangle_rows; ++i) for (int y = 2 * rectangle[i][1]; y <= 2 * rectangle[i][3]; ++y) for (int x = 2 * rectangle[i][0]; x <= 2 * rectangle[i][2]; ++x) board[y][x] = 1;
    for (size_t i = 0; i < rectangle_rows; ++i) for (int y = 2 * rectangle[i][1] + 1; y < 2 * rectangle[i][3]; ++y) for (int x = 2 * rectangle[i][0] + 1; x < 2 * rectangle[i][2]; ++x) board[y][x] = 0;
    int queue[10404], distance[10404] = {0}, head = 0, tail = 0, answer = 0;
    int start = 2 * characterY * 102 + 2 * characterX, goal = 2 * itemY * 102 + 2 * itemX; queue[tail++] = start; board[2 * characterY][2 * characterX] = 0;
    const int dx[4] = {1,-1,0,0}, dy[4] = {0,0,1,-1};
    while (head < tail) {
        int at = queue[head++], y = at / 102, x = at % 102;
        if (at == goal) { answer = distance[at] / 2; break; }
        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx >= 0 && nx < 102 && ny >= 0 && ny < 102 && board[ny][nx]) { board[ny][nx] = 0; distance[ny * 102 + nx] = distance[at] + 1; queue[tail++] = ny * 102 + nx; }
        }
    }
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
// int solution(int** rectangle, size_t rectangle_rows, size_t rectangle_cols, int characterX, int characterY, int itemX, int itemY) {  // 좌표를 두 배로 확대하고 직사각형들을 전부 채운 뒤, 각 직사각형의 내부를 모두 지워 합친 지형의 테두리를 만들기
//     (void)rectangle_cols; int board[102][102] = {{0}};  // 두 배 좌표의 외곽선 표시 갱신
//     for (size_t i = 0; i < rectangle_rows; ++i) for (int y = 2 * rectangle[i][1]; y <= 2 * rectangle[i][3]; ++y) for (int x = 2 * rectangle[i][0]; x <= 2 * rectangle[i][2]; ++x) board[y][x] = 1;  // 직사각형 번호 순서대로 확인; 현재 세로 좌표 / 현재 가로 좌표 갱신
//     for (size_t i = 0; i < rectangle_rows; ++i) for (int y = 2 * rectangle[i][1] + 1; y < 2 * rectangle[i][3]; ++y) for (int x = 2 * rectangle[i][0] + 1; x < 2 * rectangle[i][2]; ++x) board[y][x] = 0;  // 직사각형 번호 순서대로 확인; 현재 세로 좌표 / 현재 가로 좌표 갱신
//     int queue[10404], distance[10404] = {0}, head = 0, tail = 0, answer = 0;  // 두 배 격자에서의 이동 거리 / 큐에서 읽을 위치 / 큐에 넣을 위치 / 원래 좌표의 최단 거리 저장
//     int start = 2 * characterY * 102 + 2 * characterX, goal = 2 * itemY * 102 + 2 * itemX; queue[tail++] = start; board[2 * characterY][2 * characterX] = 0;  // 캐릭터 시작 좌표 / 아이템 좌표 / 외곽선 BFS 대기 칸 / 두 배 좌표의 외곽선 표시 저장
//     const int dx[4] = {1,-1,0,0}, dy[4] = {0,0,1,-1};  // 가로 이동 / 세로 이동 저장
//     while (head < tail) {  // 큐에 미처리 정점이 남아 있는 동안 너비 우선 탐색을 계속하기
//         int at = queue[head++], y = at / 102, x = at % 102;  // 현재 칸 번호 / 현재 세로 좌표 / 현재 가로 좌표 저장
//         if (at == goal) { answer = distance[at] / 2; break; }  // 아이템에 닿았으면 두 배 좌표의 거리를 2로 나눠 답 기록
//         for (int d = 0; d < 4; ++d) {  // 이동 방향 순서대로 확인
//             int nx = x + dx[d], ny = y + dy[d];  // 다음 가로 좌표 / 다음 세로 좌표 저장
//             if (nx >= 0 && nx < 102 && ny >= 0 && ny < 102 && board[ny][nx]) { board[ny][nx] = 0; distance[ny * 102 + nx] = distance[at] + 1; queue[tail++] = ny * 102 + nx; }  // 이웃 좌표가 격자 안이고 칸 조건도 맞으면 두 배 좌표의 외곽선 표시 / 두 배 격자에서의 이동 거리 / 외곽선 BFS 대기 칸 갱신
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     return answer;  // 원래 좌표의 최단 거리 반환
// }  // 이 범위 끝

// 풀이 요약
// 좌표를 두 배로 확대하고 직사각형들을 전부 채운 뒤, 각 직사각형의 내부를 모두 지워 합친 지형의 테두리를 만들기
// 테두리 위에서 BFS를 하면 최단 이동 거리; 좌표 확대 때문에 생긴 거리 두 배를 마지막에 나누기; 좌표 최대값 C에 대해 시간·공간 O(C²), 직사각형 수는 최대 4
// 예: 원래 한 칸 너비의 굴곡도 두 칸 간격으로 표현되어, 인접해 보이는 서로 다른 테두리를 가로지르는 지름길을 막기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:32:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/035_87694_%EC%95%84%EC%9D%B4%ED%85%9C_%EC%A4%8D%EA%B8%B0/README.md)
