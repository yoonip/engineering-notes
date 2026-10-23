# 지게차와 크레인

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/388353) · Level 2 · C

## 풀이

크레인은 목표 종류를 모두 제거하고, 지게차는 바깥 빈칸에서 BFS(가까운 칸부터 큐로 탐색)해 닿는 목표만 제거
한 요청의 탐색이 끝난 뒤 한꺼번에 지워, 방금 열린 통로를 같은 요청에서 사용하지 않게 하기
예: A로 가득한 3x3 창고에서 요청 A 한 번이면 바깥 8개만 빠져 1개가 남음; 시간 O(요청 수*행*열)

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

int solution(const char* storage[], size_t storage_len, const char* requests[], size_t requests_len) {
    int rows = (int)storage_len + 2, cols = (int)strlen(storage[0]) + 2, remaining = (rows - 2) * (cols - 2);
    size_t size = (size_t)rows * cols;
    char* board = malloc(size); memset(board, '.', size);
    for (int r = 1; r < rows - 1; ++r) memcpy(board + r * cols + 1, storage[r - 1], cols - 2);
    bool* visited = malloc(size * sizeof(*visited)); int* queue = malloc(size * sizeof(*queue)); int* removed = malloc(size * sizeof(*removed));
    const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (size_t i = 0; i < requests_len; ++i) {
        char target = requests[i][0]; int count = 0;
        if (requests[i][1]) {
            for (size_t at = 0; at < size; ++at) if (board[at] == target) removed[count++] = (int)at;
        } else {
            memset(visited, 0, size * sizeof(*visited)); int head = 0, tail = 0; queue[tail++] = 0; visited[0] = true;
            while (head < tail) {
                int at = queue[head++], r = at / cols, c = at % cols;
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || visited[nr * cols + nc]) continue;
                    int next = nr * cols + nc; visited[next] = true;
                    if (board[next] == '.') queue[tail++] = next;
                    else if (board[next] == target) removed[count++] = next;
                }
            }
        }
        for (int j = 0; j < count; ++j) board[removed[j]] = '.';
        remaining -= count;
    }
    free(board); free(visited); free(queue); free(removed);
    return remaining;
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
// int solution(const char* storage[], size_t storage_len, const char* requests[], size_t requests_len) {  // 크레인은 목표 종류를 모두 제거하고, 지게차는 바깥 빈칸에서 BFS(가까운 칸부터 큐로 탐색)해 닿는 목표만 제거
//     int rows = (int)storage_len + 2, cols = (int)strlen(storage[0]) + 2, remaining = (rows - 2) * (cols - 2);  // 테두리를 포함한 행 수 / 테두리를 포함한 열 수 / 남은 컨테이너 수 저장
//     size_t size = (size_t)rows * cols;  // 테두리 포함 전체 칸 수 저장
//     char* board = malloc(size); memset(board, '.', size);  // 바깥 빈칸을 덧댄 창고 공간 확보
//     for (int r = 1; r < rows - 1; ++r) memcpy(board + r * cols + 1, storage[r - 1], cols - 2);  // 현재 행 순서대로 확인; 바깥 빈칸을 덧댄 창고 / 현재 행 / 테두리를 포함한 열 수 복사
//     bool* visited = malloc(size * sizeof(*visited)); int* queue = malloc(size * sizeof(*queue)); int* removed = malloc(size * sizeof(*removed));  // 이번 바깥 탐색에서 본 칸 / 외부와 이어진 빈칸 / 이번 요청에서 꺼낼 컨테이너 위치 공간 확보
//     const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 행 이동 / 열 이동 저장
//     for (size_t i = 0; i < requests_len; ++i) {  // 꺼내기 요청 번호 순서대로 확인
//         char target = requests[i][0]; int count = 0;  // 이번에 꺼낼 컨테이너 문자 / 이번에 제거할 개수 저장
//         if (requests[i][1]) {  // 요청 문자가 두 개이면 크레인 방식으로 같은 문자를 모두 제거
//             for (size_t at = 0; at < size; ++at) if (board[at] == target) removed[count++] = (int)at;  // 현재 창고 전체에서 요청한 컨테이너 위치를 제거 목록에 모으기
//         } else {  // 한 글자 요청은 바깥에서 접근 가능한 컨테이너만 제거
//             memset(visited, 0, size * sizeof(*visited)); int head = 0, tail = 0; queue[tail++] = 0; visited[0] = true;  // 큐에서 읽을 위치 / 큐에 넣을 위치 초기화
//             while (head < tail) {  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//                 int at = queue[head++], r = at / cols, c = at % cols;  // 현재 칸 번호 / 현재 행 / 현재 열 저장
//                 for (int d = 0; d < 4; ++d) {  // 이웃 방향 순서대로 확인
//                     int nr = r + dr[d], nc = c + dc[d];  // 다음 행 / 다음 열 저장
//                     if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || visited[nr * cols + nc]) continue;  // 격자 밖이거나 막혔거나 이미 처리한 칸이면 다음 후보로 넘어가기
//                     int next = nr * cols + nc; visited[next] = true;  // 다음 칸 번호 / 이번 바깥 탐색에서 본 칸 저장
//                     if (board[next] == '.') queue[tail++] = next;  // 빈칸이면 바깥에서 이어지는 공간이므로 탐색 큐에 추가
//                     else if (board[next] == target) removed[count++] = next;  // 바깥에서 닿은 요청 컨테이너를 이번 제거 목록에 추가
//                 }  // 이 범위 끝
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         for (int j = 0; j < count; ++j) board[removed[j]] = '.';  // 제거 목록 위치 순서대로 확인; 바깥 빈칸을 덧댄 창고 / 이번 요청에서 꺼낼 컨테이너 위치 / 제거 목록 위치 확인
//         remaining -= count;  // 남은 컨테이너 수 / 이번에 제거할 개수에서 이번 사용량 빼기
//     }  // 이 범위 끝
//     free(board); free(visited); free(queue); free(removed);  // 바깥 빈칸을 덧댄 창고 / 이번 바깥 탐색에서 본 칸 / 외부와 이어진 빈칸 / 이번 요청에서 꺼낼 컨테이너 위치 임시 공간 정리
//     return remaining;  // 남은 컨테이너 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 크레인은 목표 종류를 모두 제거하고, 지게차는 바깥 빈칸에서 BFS(가까운 칸부터 큐로 탐색)해 닿는 목표만 제거
// 한 요청의 탐색이 끝난 뒤 한꺼번에 지워, 방금 열린 통로를 같은 요청에서 사용하지 않게 하기
// 예: A로 가득한 3x3 창고에서 요청 A 한 번이면 바깥 8개만 빠져 1개가 남음; 시간 O(요청 수*행*열)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:07:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/007_388353_%EC%A7%80%EA%B2%8C%EC%B0%A8%EC%99%80_%ED%81%AC%EB%A0%88%EC%9D%B8/README.md)
