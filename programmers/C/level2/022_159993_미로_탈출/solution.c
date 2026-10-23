#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int bfs(const char** maps, int rows, int cols, int start, int goal) {
    int* distance = malloc((size_t)rows * cols * sizeof(*distance)); int* queue = malloc((size_t)rows * cols * sizeof(*queue));
    for (int i = 0; i < rows * cols; ++i) distance[i] = -1;
    int head = 0, tail = 0; queue[tail++] = start; distance[start] = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (head < tail) {
        int at = queue[head++], r = at / cols, c = at % cols;
        if (at == goal) break;
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maps[nr][nc] != 'X' && distance[nr * cols + nc] == -1) {
                distance[nr * cols + nc] = distance[at] + 1; queue[tail++] = nr * cols + nc;
            }
        }
    }
    int answer = distance[goal]; free(distance); free(queue);
    return answer;
}
int solution(const char* maps[], size_t maps_len) {
    int rows = (int)maps_len, cols = (int)strlen(maps[0]), start = 0, lever = 0, exit = 0;
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        if (maps[r][c] == 'S') start = r * cols + c;
        if (maps[r][c] == 'L') lever = r * cols + c;
        if (maps[r][c] == 'E') exit = r * cols + c;
    }
    int first = bfs(maps, rows, cols, start, lever), second = bfs(maps, rows, cols, lever, exit);
    return first < 0 || second < 0 ? -1 : first + second;
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
// static int bfs(const char** maps, int rows, int cols, int start, int goal) {  // 큐를 사용하여 시작점부터 목표점까지의 최단 거리를 구하는 보조 함수를 정의하기
//     int* distance = malloc((size_t)rows * cols * sizeof(*distance)); int* queue = malloc((size_t)rows * cols * sizeof(*queue));  // 시작점부터의 최단 거리 / 갈 수 있는 미로 칸 공간 확보
//     for (int i = 0; i < rows * cols; ++i) distance[i] = -1;  // 거리 초기화 위치 순서대로 확인; 시작점부터의 최단 거리 갱신
//     int head = 0, tail = 0; queue[tail++] = start; distance[start] = 0; const int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 시작점 거리를 0으로 두고 탐색 큐에 추가; 네 방향 이동값 설정
//     while (head < tail) {  // 큐에 미처리 위치가 남아 있는 동안 너비 우선 탐색을 계속하기
//         int at = queue[head++], r = at / cols, c = at % cols;  // 현재 칸 번호 / 현재 행 / 현재 열 저장
//         if (at == goal) break;  // 목표 칸을 꺼냈으면 최단 거리를 찾았으므로 탐색 종료
//         for (int d = 0; d < 4; ++d) {  // 이웃 방향 번호 순서대로 확인
//             int nr = r + dr[d], nc = c + dc[d];  // 다음 행 / 다음 열 저장
//             if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && maps[nr][nc] != 'X' && distance[nr * cols + nc] == -1) {  // 격자 안의 아직 안 간 이동 가능한 칸이면 처리
//                 distance[nr * cols + nc] = distance[at] + 1; queue[tail++] = nr * cols + nc;  // 시작점부터의 최단 거리 / 갈 수 있는 미로 칸 갱신
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     int answer = distance[goal]; free(distance); free(queue);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 레버를 거치는 최소 이동 수 반환
// }  // 이 범위 끝
// int solution(const char* maps[], size_t maps_len) {  // 시작→레버와 레버→출구의 최단 거리를 각각 BFS로 구해 더하기; 어느 한 경로라도 없으면 탈출 불가
//     int rows = (int)maps_len, cols = (int)strlen(maps[0]), start = 0, lever = 0, exit = 0;  // 미로 행 수 / 미로 열 수 / 시작점 S / 레버 L / 출구 E 저장
//     for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 현재 행 순서대로 확인; 현재 열 갱신
//         if (maps[r][c] == 'S') start = r * cols + c;  // S 칸의 일차원 위치를 시작점으로 기록
//         if (maps[r][c] == 'L') lever = r * cols + c;  // L 칸의 일차원 위치를 레버 위치로 기록
//         if (maps[r][c] == 'E') exit = r * cols + c;  // E 칸의 일차원 위치를 출구로 기록
//     }  // 이 범위 끝
//     int first = bfs(maps, rows, cols, start, lever), second = bfs(maps, rows, cols, lever, exit);  // S에서 L까지의 거리 / L에서 E까지의 거리 저장
//     return first < 0 || second < 0 ? -1 : first + second;  // S에서 L까지의 거리 / L에서 E까지의 거리로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 시작→레버와 레버→출구의 최단 거리를 각각 BFS로 구해 더하기; 어느 한 경로라도 없으면 탈출 불가
// 예: 첫 미로는 4+12=16초.; 레버 전에도 출구 칸은 통과할 수 있음; 시간·공간 O(행*열)
