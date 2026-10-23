#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static int distances(int start, int n, const int* head, const int* to, const int* next, int* distance, int* queue, int* count) {
    for (int i = 0; i <= n; ++i) distance[i] = -1; int first = 0, last = 0; queue[last++] = start; distance[start] = 0;
    while (first < last) { int node = queue[first++]; for (int e = head[node]; e >= 0; e = next[e]) if (distance[to[e]] < 0) { distance[to[e]] = distance[node] + 1; queue[last++] = to[e]; } }
    int farthest = start; *count = 0;
    for (int i = 1; i <= n; ++i) if (distance[i] > distance[farthest]) farthest = i;
    for (int i = 1; i <= n; ++i) *count += distance[i] == distance[farthest];
    return farthest;
}
int solution(int n, int** edges, size_t edges_rows, size_t edges_cols) {
    (void)edges_cols; int* head = malloc(((size_t)n + 1) * sizeof(*head)); int* to = malloc(2 * edges_rows * sizeof(*to)); int* next = malloc(2 * edges_rows * sizeof(*next)); int* distance = malloc(((size_t)n + 1) * sizeof(*distance)); int* queue = malloc((size_t)n * sizeof(*queue));
    for (int i = 0; i <= n; ++i) head[i] = -1; int total = 0;
    for (size_t i = 0; i < edges_rows; ++i) for (int d = 0; d < 2; ++d) { int a = edges[i][d], b = edges[i][1 - d]; to[total] = b; next[total] = head[a]; head[a] = total++; }
    int count = 0, first = distances(1,n,head,to,next,distance,queue,&count), second = distances(first,n,head,to,next,distance,queue,&count), diameter = distance[second], answer = diameter;
    if (count < 2) { distances(second,n,head,to,next,distance,queue,&count); if (count < 2) answer = diameter - 1; }
    free(head); free(to); free(next); free(distance); free(queue);
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
// static int distances(int start, int n, const int* head, const int* to, const int* next, int* distance, int* queue, int* count) {  // 큐를 이용한 너비 우선 탐색으로 도달 가능성 또는 최단 거리를 계산
//     for (int i = 0; i <= n; ++i) distance[i] = -1; int first = 0, last = 0; queue[last++] = start; distance[start] = 0;  // 정점 또는 간선 번호 순서대로 확인; 시작점에서 각 정점까지의 거리 / 지름의 첫 끝점 / BFS 대기 정점 갱신
//     while (first < last) { int node = queue[first++]; for (int e = head[node]; e >= 0; e = next[e]) if (distance[to[e]] < 0) { distance[to[e]] = distance[node] + 1; queue[last++] = to[e]; } }  // 큐에 미처리 정점이 남아 있는 동안 너비 우선 탐색을 계속하기
//     int farthest = start; *count = 0;  // 가장 먼 정점 / 최대 거리에 있는 정점 수 저장
//     for (int i = 1; i <= n; ++i) if (distance[i] > distance[farthest]) farthest = i;  // 시작점에서 가장 멀리 떨어진 노드 찾기
//     for (int i = 1; i <= n; ++i) *count += distance[i] == distance[farthest];  // 정점 또는 간선 번호 순서대로 확인; 최대 거리에 있는 정점 수 / 시작점에서 각 정점까지의 거리 / 정점 또는 간선 번호 더해 누적
//     return farthest;  // 가장 먼 정점 반환
// }  // 이 범위 끝
// int solution(int n, int** edges, size_t edges_rows, size_t edges_cols) {  // BFS로 지름 양 끝점을 찾기; 어느 한 끝점에서 지름 거리의 정점이 둘 이상이면 두 거리가 지름인 세 점을 고를 수 있음
//     (void)edges_cols; int* head = malloc(((size_t)n + 1) * sizeof(*head)); int* to = malloc(2 * edges_rows * sizeof(*to)); int* next = malloc(2 * edges_rows * sizeof(*next)); int* distance = malloc(((size_t)n + 1) * sizeof(*distance)); int* queue = malloc((size_t)n * sizeof(*queue));  // 정점별 첫 트리 간선 / 연결된 정점 / 같은 정점의 다음 간선 / 시작점에서 각 정점까지의 거리 공간 확보
//     for (int i = 0; i <= n; ++i) head[i] = -1; int total = 0;  // 정점 또는 간선 번호 순서대로 확인; 정점별 첫 트리 간선 / 저장한 양방향 간선 수 갱신
//     for (size_t i = 0; i < edges_rows; ++i) for (int d = 0; d < 2; ++d) { int a = edges[i][d], b = edges[i][1 - d]; to[total] = b; next[total] = head[a]; head[a] = total++; }  // 정점 또는 간선 번호 순서대로 확인; 양방향 방향 / 저장한 양방향 간선 수 갱신
//     int count = 0, first = distances(1,n,head,to,next,distance,queue,&count), second = distances(first,n,head,to,next,distance,queue,&count), diameter = distance[second], answer = diameter;  // 최대 거리에 있는 정점 수 / 지름의 첫 끝점 / 지름의 둘째 끝점 / 트리 지름 길이 / 세 정점 거리 중간값의 최댓값 저장
//     if (count < 2) { distances(second,n,head,to,next,distance,queue,&count); if (count < 2) answer = diameter - 1; }  // 최대 거리에 있는 정점 수가 2보다 작으면 세 정점 거리 중간값의 최댓값 갱신
//     free(head); free(to); free(next); free(distance); free(queue);  // 정점별 첫 트리 간선 / 연결된 정점 / 같은 정점의 다음 간선 / 시작점에서 각 정점까지의 거리 임시 공간 정리
//     return answer;  // 세 정점 거리 중간값의 최댓값 반환
// }  // 이 범위 끝

// 풀이 요약
// BFS로 지름 양 끝점을 찾기; 어느 한 끝점에서 지름 거리의 정점이 둘 이상이면 두 거리가 지름인 세 점을 고를 수 있음
// 그렇지 않으면 지름 경로에서 끝점 바로 옆 점을 세 번째 점으로 골라 지름-1을 얻기; 예: 4점 일자 트리는 2, 별 모양은 2
// BFS를 최대 세 번 수행하기; 시간·공간 O(n)
