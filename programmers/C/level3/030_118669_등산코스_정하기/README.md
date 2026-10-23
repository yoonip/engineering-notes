# 등산코스 정하기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/118669) · Level 3 · C

## 풀이

허용할 산길 강도를 이분 탐색하고, 그 이하 간선만 쓰는 다중 시작점 BFS로 산봉우리 도달 여부 확인
산봉우리에 도달하면 그 뒤로 확장하지 않기; 가능한 최소 강도를 찾은 뒤 도달한 산봉우리 중 최소 번호 선택; 최대 강도 W일 때 시간 O((N+E) log(W+1)), 공간 O(N+E)
예: 간선이 3·2·3인 코스는 합 8이 아니라 intensity 3; 같은 intensity라면 산봉우리 번호가 작은 코스를 고르기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int to, weight, next; } Edge;
static int reachable(int n, const int* head, const Edge* edges, const bool* summit, const int* gates, size_t gates_len, int limit, bool* visited, int* queue) {
    memset(visited, 0, ((size_t)n + 1) * sizeof(*visited)); int first = 0, last = 0, best = 0;
    for (size_t i = 0; i < gates_len; ++i) { visited[gates[i]] = true; queue[last++] = gates[i]; }
    while (first < last) {
        int node = queue[first++];
        if (summit[node]) { if (!best || node < best) best = node; continue; }
        for (int e = head[node]; e >= 0; e = edges[e].next) if (edges[e].weight <= limit && !visited[edges[e].to]) { visited[edges[e].to] = true; queue[last++] = edges[e].to; }
    }
    return best;
}
int* solution(int n, int** paths, size_t paths_rows, size_t paths_cols, int gates[], size_t gates_len, int summits[], size_t summits_len) {
    (void)paths_cols; int* head = malloc(((size_t)n + 1) * sizeof(*head)); Edge* edges = malloc(2 * paths_rows * sizeof(*edges)); bool* summit = calloc((size_t)n + 1, sizeof(*summit));
    bool* visited = malloc(((size_t)n + 1) * sizeof(*visited)); int* queue = malloc(((size_t)n + 1) * sizeof(*queue)); for (int i = 0; i <= n; ++i) head[i] = -1;
    int count = 0, low = 0, high = 0;
    for (size_t i = 0; i < paths_rows; ++i) { if (paths[i][2] > high) high = paths[i][2]; for (int d = 0; d < 2; ++d) { int a = paths[i][d], b = paths[i][1 - d]; edges[count] = (Edge){b,paths[i][2],head[a]}; head[a] = count++; } }
    for (size_t i = 0; i < summits_len; ++i) summit[summits[i]] = true;
    while (low < high) { int mid = low + (high - low) / 2; if (reachable(n,head,edges,summit,gates,gates_len,mid,visited,queue)) high = mid; else low = mid + 1; }
    int* answer = malloc(2 * sizeof(*answer)); answer[0] = reachable(n,head,edges,summit,gates,gates_len,low,visited,queue); answer[1] = low;
    free(head); free(edges); free(summit); free(visited); free(queue);
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
// typedef struct { int to, weight, next; } Edge;  // 도착 정점·산길 강도·다음 간선 번호를 한 항목으로 묶기
// static int reachable(int n, const int* head, const Edge* edges, const bool* summit, const int* gates, size_t gates_len, int limit, bool* visited, int* queue) {  // 큐를 이용한 너비 우선 탐색으로 도달 가능성 또는 최단 거리를 계산
//     memset(visited, 0, ((size_t)n + 1) * sizeof(*visited)); int first = 0, last = 0, best = 0;  // 큐에서 읽을 위치 / 큐에 넣을 위치 초기화
//     for (size_t i = 0; i < gates_len; ++i) { visited[gates[i]] = true; queue[last++] = gates[i]; }  // 산길 또는 출입구 위치 순서대로 확인; 큐에 넣을 위치 갱신
//     while (first < last) {  // 큐에 미처리 정점이 남아 있는 동안 너비 우선 탐색을 계속하기
//         int node = queue[first++];  // 현재 산길 정점 저장
//         if (summit[node]) { if (!best || node < best) best = node; continue; }  // 산봉우리에 도착하면 최소 번호만 갱신하고 더 지나가지 않기
//         for (int e = head[node]; e >= 0; e = edges[e].next) if (edges[e].weight <= limit && !visited[edges[e].to]) { visited[edges[e].to] = true; queue[last++] = edges[e].to; }  // 제한 이하 간선으로 이어지고 아직 안 간 노드만 큐에 추가
//     }  // 이 범위 끝
//     return best;  // 도달한 산봉우리 중 최소 번호 반환
// }  // 이 범위 끝
// int* solution(int n, int** paths, size_t paths_rows, size_t paths_cols, int gates[], size_t gates_len, int summits[], size_t summits_len) {  // 허용할 산길 강도를 이분 탐색하고, 그 이하 간선만 쓰는 다중 시작점 BFS로 산봉우리 도달 여부 확인
//     (void)paths_cols; int* head = malloc(((size_t)n + 1) * sizeof(*head)); Edge* edges = malloc(2 * paths_rows * sizeof(*edges)); bool* summit = calloc((size_t)n + 1, sizeof(*summit));  // 노드별 첫 산길 / 양방향 산길 목록 / 산봉우리 표시 공간 확보하고 0으로 시작
//     bool* visited = malloc(((size_t)n + 1) * sizeof(*visited)); int* queue = malloc(((size_t)n + 1) * sizeof(*queue)); for (int i = 0; i <= n; ++i) head[i] = -1;  // 현재 강도로 갈 수 있는 정점 / 다중 출발 BFS 큐 / 산길 또는 출입구 위치 / 노드별 첫 산길 공간 확보
//     int count = 0, low = 0, high = 0;  // 저장한 방향 간선 수 / 가능한 최대 경사 하한 / 최대 경사 상한 저장
//     for (size_t i = 0; i < paths_rows; ++i) { if (paths[i][2] > high) high = paths[i][2]; for (int d = 0; d < 2; ++d) { int a = paths[i][d], b = paths[i][1 - d]; edges[count] = (Edge){b,paths[i][2],head[a]}; head[a] = count++; } }  // 산길 또는 출입구 위치 순서대로 확인; 양방향 간선 방향 / 저장한 방향 간선 수 갱신
//     for (size_t i = 0; i < summits_len; ++i) summit[summits[i]] = true;  // 산길 또는 출입구 위치 순서대로 확인; 산봉우리 표시 / 산길 또는 출입구 위치 확인
//     while (low < high) { int mid = low + (high - low) / 2; if (reachable(n,head,edges,summit,gates,gates_len,mid,visited,queue)) high = mid; else low = mid + 1; }  // 이분 탐색 범위가 한 값으로 좁혀질 때까지 가능 여부를 확인
//     int* answer = malloc(2 * sizeof(*answer)); answer[0] = reachable(n,head,edges,summit,gates,gates_len,low,visited,queue); answer[1] = low;  // 선택한 산봉우리와 최소 강도 공간 확보
//     free(head); free(edges); free(summit); free(visited); free(queue);  // 노드별 첫 산길 / 양방향 산길 목록 / 산봉우리 표시 / 현재 강도로 갈 수 있는 정점 임시 공간 정리
//     return answer;  // 선택한 산봉우리와 최소 강도 반환
// }  // 이 범위 끝

// 풀이 요약
// 허용할 산길 강도를 이분 탐색하고, 그 이하 간선만 쓰는 다중 시작점 BFS로 산봉우리 도달 여부 확인
// 산봉우리에 도달하면 그 뒤로 확장하지 않기; 가능한 최소 강도를 찾은 뒤 도달한 산봉우리 중 최소 번호 선택; 최대 강도 W일 때 시간 O((N+E) log(W+1)), 공간 O(N+E)
// 예: 간선이 3·2·3인 코스는 합 8이 아니라 intensity 3; 같은 intensity라면 산봉우리 번호가 작은 코스를 고르기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/030_118669_%EB%93%B1%EC%82%B0%EC%BD%94%EC%8A%A4_%EC%A0%95%ED%95%98%EA%B8%B0/README.md)
