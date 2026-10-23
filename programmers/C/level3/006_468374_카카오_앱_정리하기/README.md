# 카카오 앱 정리하기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468374) · Level 3 · C

## 풀이

앱은 왼쪽 위 좌표와 한 변 길이로 관리하기; 한 바퀴를 넘는 좌표를 그대로 유지해 앱 사이의 앞뒤 순서를 보존하고, 일부가 격자를 벗어나면 다음 바퀴의 시작으로 넘기기
서로 밀 수 있는 앱 사이에 최소 간격 조건을 만들고, 더 밀려야 하는 앱의 좌표를 큐로 전파하기; 반대편에서 돌아온 앱이 이전 앱을 다시 미는 효과도 같은 조건으로 처리
예: 2x2 앱이 세로 2칸 격자에서 위로 움직이면 시작 행은 계속 0; 왼쪽 끝에서 왼쪽으로 밀면 시작 열이 가능한 최댓값으로 바뀜

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int row, col, size; } App;
static long long normalize(long long value, int length, int size) {
    long long remainder = value % length; if (remainder < 0) remainder += length;
    if (remainder > length - size) value += length - remainder;
    return value;
}
int** solution(int** board, size_t board_rows, size_t board_cols, int** commands, size_t commands_rows, size_t commands_cols) {
    (void)commands_cols; int count = 0;
    for (size_t r = 0; r < board_rows; ++r) for (size_t c = 0; c < board_cols; ++c) if (board[r][c] > count) count = board[r][c];
    App* apps = calloc((size_t)count, sizeof(*apps)); bool* found = calloc((size_t)count, sizeof(*found));
    for (int r = 0; r < (int)board_rows; ++r) for (int c = 0; c < (int)board_cols; ++c) if (board[r][c]) {
        int number = board[r][c] - 1;
        if (!found[number]) { found[number] = true; apps[number] = (App){r,c,1}; }
        else { int extent = r - apps[number].row + 1; if (c - apps[number].col + 1 > extent) extent = c - apps[number].col + 1; if (extent > apps[number].size) apps[number].size = extent; }
    }
    long long* positions = malloc((size_t)count * sizeof(*positions)); int* gaps = malloc((size_t)count * count * sizeof(*gaps)); bool* queued = malloc((size_t)count * sizeof(*queued)); int* queue = malloc(((size_t)count + 1) * sizeof(*queue));
    for (size_t command = 0; command < commands_rows; ++command) {
        int number = commands[command][0] - 1, direction = commands[command][1], axis = direction % 2, length = axis ? (int)board_cols : (int)board_rows; bool reverse = direction >= 3;
        for (int i = 0; i < count; ++i) { int coordinate = axis ? apps[i].col : apps[i].row; positions[i] = reverse ? length - apps[i].size - coordinate : coordinate; }
        for (int i = 0; i < count * count; ++i) gaps[i] = INT_MIN;
        for (int i = 0; i < count; ++i) for (int j = 0; j < i; ++j) {
            int side_i = axis ? apps[i].row : apps[i].col, side_j = axis ? apps[j].row : apps[j].col;
            if (side_i >= side_j + apps[j].size || side_j >= side_i + apps[i].size) continue;
            int first = positions[i] < positions[j] ? i : j, second = first == i ? j : i;
            gaps[first * count + second] = apps[first].size; gaps[second * count + first] = apps[second].size - length;
        }
        positions[number] = normalize(positions[number] + 1,length,apps[number].size); memset(queued,0,(size_t)count * sizeof(*queued));
        int first = 0, last = 0, capacity = count + 1; queue[last++] = number; queued[number] = true;
        while (first != last) {
            int current = queue[first]; first = (first + 1) % capacity; queued[current] = false;
            for (int other = 0; other < count; ++other) if (gaps[current * count + other] != INT_MIN) {
                long long needed = normalize(positions[current] + gaps[current * count + other],length,apps[other].size);
                if (needed > positions[other]) { positions[other] = needed; if (!queued[other]) { queued[other] = true; queue[last] = other; last = (last + 1) % capacity; } }
            }
        }
        for (int i = 0; i < count; ++i) { int coordinate = (int)(positions[i] % length); if (reverse) coordinate = length - apps[i].size - coordinate; if (axis) apps[i].col = coordinate; else apps[i].row = coordinate; }
    }
    int** answer = malloc(board_rows * sizeof(*answer)); for (size_t r = 0; r < board_rows; ++r) answer[r] = calloc(board_cols,sizeof(**answer));
    for (int i = 0; i < count; ++i) for (int r = apps[i].row; r < apps[i].row + apps[i].size; ++r) for (int c = apps[i].col; c < apps[i].col + apps[i].size; ++c) answer[r][c] = i + 1;
    free(apps); free(found); free(positions); free(gaps); free(queued); free(queue);
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
// typedef struct { int row, col, size; } App;  // 앱의 왼쪽 위 행·열과 정사각형 한 변 길이 보관
// static long long normalize(long long value, int length, int size) {  // 앱이 경계에 걸치면 다음 순환 위치로 넘기기
//     long long remainder = value % length; if (remainder < 0) remainder += length;  // 축 길이로 나눈 순환 좌표 저장
//     if (remainder > length - size) value += length - remainder;  // 앱이 순환 경계를 넘으면 다음 줄 또는 열의 시작으로 넘기기
//     return value;  // 앱이 경계에 걸치지 않게 보정한 순환 좌표 반환
// }  // 이 범위 끝
// int** solution(int** board, size_t board_rows, size_t board_cols, int** commands, size_t commands_rows, size_t commands_cols) {  // 앱은 왼쪽 위 좌표와 한 변 길이로 관리하기; 한 바퀴를 넘는 좌표를 그대로 유지해 앱 사이의 앞뒤 순서를 보존하고, 일부가 격자를 벗어나면 다음 바퀴의 시작으로 넘기기
//     (void)commands_cols; int count = 0;  // 앱 개수 갱신
//     for (size_t r = 0; r < board_rows; ++r) for (size_t c = 0; c < board_cols; ++c) if (board[r][c] > count) count = board[r][c];  // 보드 행 순서대로 확인; 보드 열 갱신
//     App* apps = calloc((size_t)count, sizeof(*apps)); bool* found = calloc((size_t)count, sizeof(*found));  // 앱별 왼쪽 위와 한 변 크기 / 앱을 처음 발견했는지 표시 공간 확보하고 0으로 시작
//     for (int r = 0; r < (int)board_rows; ++r) for (int c = 0; c < (int)board_cols; ++c) if (board[r][c]) {  // 보드 행 순서대로 확인; 보드 열 갱신
//         int number = board[r][c] - 1;  // 이번에 움직일 앱 번호 저장
//         if (!found[number]) { found[number] = true; apps[number] = (App){r,c,1}; }  // 처음 본 앱 번호의 시작 위치와 크기 1 저장
//         else { int extent = r - apps[number].row + 1; if (c - apps[number].col + 1 > extent) extent = c - apps[number].col + 1; if (extent > apps[number].size) apps[number].size = extent; }  // 앞 조건이 아니면 현재 앱에서 확인한 가장 먼 크기 저장
//     }  // 이 범위 끝
//     long long* positions = malloc((size_t)count * sizeof(*positions)); int* gaps = malloc((size_t)count * count * sizeof(*gaps)); bool* queued = malloc((size_t)count * sizeof(*queued)); int* queue = malloc(((size_t)count + 1) * sizeof(*queue));  // 밀기 방향으로 바꾼 앱 좌표 / 앱 사이 필요한 최소 간격 / 전파 큐에 들어 있는 앱 / 겹침 때문에 더 밀어야 할 앱 공간 확보
//     for (size_t command = 0; command < commands_rows; ++command) {  // 명령 위치 순서대로 확인
//         int number = commands[command][0] - 1, direction = commands[command][1], axis = direction % 2, length = axis ? (int)board_cols : (int)board_rows; bool reverse = direction >= 3;  // 이번에 움직일 앱 번호 / 명령 방향 / 움직일 행 또는 열 축 / 이동 축의 보드 길이 / 반대쪽 좌표로 바꿀 방향인지 여부 저장
//         for (int i = 0; i < count; ++i) { int coordinate = axis ? apps[i].col : apps[i].row; positions[i] = reverse ? length - apps[i].size - coordinate : coordinate; }  // 앱 번호 순서대로 확인; 원래 보드로 돌릴 좌표 / 밀기 방향으로 바꾼 앱 좌표 저장
//         for (int i = 0; i < count * count; ++i) gaps[i] = INT_MIN;  // 앱 번호 순서대로 확인; 앱 사이 필요한 최소 간격 갱신
//         for (int i = 0; i < count; ++i) for (int j = 0; j < i; ++j) {  // 앱 번호 순서대로 확인; 비교할 다른 앱 갱신
//             int side_i = axis ? apps[i].row : apps[i].col, side_j = axis ? apps[j].row : apps[j].col;  // 첫 앱의 수직 축 위치 / 둘째 앱의 수직 축 위치 저장
//             if (side_i >= side_j + apps[j].size || side_j >= side_i + apps[i].size) continue;  // 밀리는 축과 수직인 구간이 겹치지 않는 앱끼리는 충돌 관계에서 제외
//             int first = positions[i] < positions[j] ? i : j, second = first == i ? j : i;  // 밀기 방향에서 앞에 있는 앱 / 뒤에 있는 앱 저장
//             gaps[first * count + second] = apps[first].size; gaps[second * count + first] = apps[second].size - length;  // 앱 사이 필요한 최소 간격 갱신
//         }  // 이 범위 끝
//         positions[number] = normalize(positions[number] + 1,length,apps[number].size); memset(queued,0,(size_t)count * sizeof(*queued));  // 밀기 방향으로 바꾼 앱 좌표 초기화
//         int first = 0, last = 0, capacity = count + 1; queue[last++] = number; queued[number] = true;  // 밀기 방향에서 앞에 있는 앱 / 겹침 때문에 더 밀어야 할 앱 / 전파 큐에 들어 있는 앱 저장
//         while (first != last) {  // 전파할 위치 변경이 큐에 남아 있는 동안 충돌 해결
//             int current = queue[first]; first = (first + 1) % capacity; queued[current] = false;  // 현재 밀림을 전파할 앱 / 밀기 방향에서 앞에 있는 앱 / 전파 큐에 들어 있는 앱 저장
//             for (int other = 0; other < count; ++other) if (gaps[current * count + other] != INT_MIN) {  // 실제 충돌 관계가 있는 앱에만 위치 변경 전파
//                 long long needed = normalize(positions[current] + gaps[current * count + other],length,apps[other].size);  // 다른 앱이 밀려야 하는 최소 좌표 저장
//                 if (needed > positions[other]) { positions[other] = needed; if (!queued[other]) { queued[other] = true; queue[last] = other; last = (last + 1) % capacity; } }  // 충돌 앱을 더 밀어야 하면 위치를 갱신하고 전파 큐에 한 번만 추가
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         for (int i = 0; i < count; ++i) { int coordinate = (int)(positions[i] % length); if (reverse) coordinate = length - apps[i].size - coordinate; if (axis) apps[i].col = coordinate; else apps[i].row = coordinate; }  // 앱 번호 순서대로 확인; 원래 보드로 돌릴 좌표 저장
//     }  // 이 범위 끝
//     int** answer = malloc(board_rows * sizeof(*answer)); for (size_t r = 0; r < board_rows; ++r) answer[r] = calloc(board_cols,sizeof(**answer));  // 모든 이동을 반영한 앱 보드 / 보드 행 공간 확보하고 0으로 시작
//     for (int i = 0; i < count; ++i) for (int r = apps[i].row; r < apps[i].row + apps[i].size; ++r) for (int c = apps[i].col; c < apps[i].col + apps[i].size; ++c) answer[r][c] = i + 1;  // 앱 번호 순서대로 확인; 보드 행 / 보드 열 갱신
//     free(apps); free(found); free(positions); free(gaps); free(queued); free(queue);  // 앱별 왼쪽 위와 한 변 크기 / 앱을 처음 발견했는지 표시 / 밀기 방향으로 바꾼 앱 좌표 / 앱 사이 필요한 최소 간격 임시 공간 정리
//     return answer;  // 모든 이동을 반영한 앱 보드 반환
// }  // 이 범위 끝

// 풀이 요약
// 앱은 왼쪽 위 좌표와 한 변 길이로 관리하기; 한 바퀴를 넘는 좌표를 그대로 유지해 앱 사이의 앞뒤 순서를 보존하고, 일부가 격자를 벗어나면 다음 바퀴의 시작으로 넘기기
// 서로 밀 수 있는 앱 사이에 최소 간격 조건을 만들고, 더 밀려야 하는 앱의 좌표를 큐로 전파하기; 반대편에서 돌아온 앱이 이전 앱을 다시 미는 효과도 같은 조건으로 처리
// 예: 2x2 앱이 세로 2칸 격자에서 위로 움직이면 시작 행은 계속 0; 왼쪽 끝에서 왼쪽으로 밀면 시작 열이 가능한 최댓값으로 바뀜
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/006_468374_%EC%B9%B4%EC%B9%B4%EC%98%A4_%EC%95%B1_%EC%A0%95%EB%A6%AC%ED%95%98%EA%B8%B0/README.md)
