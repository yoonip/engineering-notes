# 중요한 도로 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/214293?language=c)

레벨 5 · C

## 풀이 요약

1번과 n번에서 다익스트라를 한 번씩 실행해 현재 최단 시간 D와 양끝 거리 계산

교통량을 0으로 내렸을 때 dist1[u]+L+distN[v] 또는 반대 방향이 D보다 작으면 감소에 민감한 도로

현재 최단 경로에 속하는 도로만 모은 부분 그래프에서 단절선을 찾으면 증가에 민감한 도로

모든 부분 그래프 도로는 실제 최단 경로에 들어가고 길이가 양수이므로, 단절선과 모든 최단 경로가 지나는 도로가 일치

두 조건 중 하나라도 만족하는 도로 번호를 오름차순으로 반환하고 없으면 [-1]

거리 합은 long long, DFS는 반복 스택 사용; 정점 N·도로 M에 대해 시간 O((N+M) log N), 공간 O(N+M)

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stddef.h>
#include <stdlib.h>
#include <stdbool.h>
#include <limits.h>

typedef struct { int to, next, id; long long weight; } Edge;
typedef struct { long long distance; int node; } State;

static void push(State* heap, int* count, State value) {
    int at = ++*count;
    while (at > 1 && heap[at / 2].distance > value.distance) {
        heap[at] = heap[at / 2];
        at /= 2;
    }
    heap[at] = value;
}

static State pop(State* heap, int* count) {
    State result = heap[1], value = heap[(*count)--];
    int at = 1;
    while (at * 2 <= *count) {
        int child = at * 2;
        if (child + 1 <= *count && heap[child + 1].distance < heap[child].distance) ++child;
        if (value.distance <= heap[child].distance) break;
        heap[at] = heap[child];
        at = child;
    }
    if (*count) heap[at] = value;
    return result;
}

static void shortest(int n, int start, const int* head, const Edge* edges, State* heap, long long* distance) {
    for (int node = 1; node <= n; ++node) distance[node] = LLONG_MAX / 4;
    int count = 0;
    distance[start] = 0;
    push(heap, &count, (State){0, start});
    while (count) {
        State current = pop(heap, &count);
        if (current.distance != distance[current.node]) continue;
        for (int arc = head[current.node]; arc != -1; arc = edges[arc].next) {
            int next = edges[arc].to;
            long long candidate = current.distance + edges[arc].weight;
            if (candidate < distance[next]) {
                distance[next] = candidate;
                push(heap, &count, (State){candidate, next});
            }
        }
    }
}

int* solution(int n, int** roads, size_t roads_rows, size_t roads_cols) {
    (void)roads_cols;
    int m = (int)roads_rows;
    int* head = malloc(((size_t)n + 1) * sizeof(*head));
    Edge* edges = malloc((size_t)2 * m * sizeof(*edges));
    for (int node = 1; node <= n; ++node) head[node] = -1;
    for (int id = 0; id < m; ++id) {
        int u = roads[id][0], v = roads[id][1];
        long long weight = (long long)roads[id][2] + roads[id][3];
        edges[2 * id] = (Edge){v, head[u], id, weight};
        head[u] = 2 * id;
        edges[2 * id + 1] = (Edge){u, head[v], id, weight};
        head[v] = 2 * id + 1;
    }
    long long* from = malloc(((size_t)n + 1) * sizeof(*from));
    long long* to = malloc(((size_t)n + 1) * sizeof(*to));
    State* heap = malloc(((size_t)2 * m + 2) * sizeof(*heap));
    shortest(n, 1, head, edges, heap, from);
    shortest(n, n, head, edges, heap, to);
    long long best = from[n];
    bool* on_path = calloc(roads_rows, sizeof(*on_path));
    bool* important = calloc(roads_rows, sizeof(*important));
    for (int id = 0; id < m; ++id) {
        int u = roads[id][0], v = roads[id][1];
        long long length = roads[id][2], weight = length + roads[id][3];
        important[id] = from[u] + length + to[v] < best || from[v] + length + to[u] < best;
        on_path[id] = from[u] + weight + to[v] == best || from[v] + weight + to[u] == best;
    }
    int* entered = calloc((size_t)n + 1, sizeof(*entered));
    int* low = malloc(((size_t)n + 1) * sizeof(*low));
    int* parent = calloc((size_t)n + 1, sizeof(*parent));
    int* parent_edge = malloc(((size_t)n + 1) * sizeof(*parent_edge));
    int* next_arc = malloc(((size_t)n + 1) * sizeof(*next_arc));
    int* stack = malloc((size_t)n * sizeof(*stack));
    int top = 0, timer = 1;
    stack[top++] = 1;
    entered[1] = low[1] = timer;
    parent_edge[1] = -1;
    next_arc[1] = head[1];
    while (top) {
        int node = stack[top - 1];
        int arc = next_arc[node];
        while (arc != -1 && !on_path[edges[arc].id]) arc = edges[arc].next;
        if (arc == -1) {
            --top;
            int p = parent[node];
            if (p) {
                if (low[node] > entered[p]) important[parent_edge[node]] = true;
                if (low[node] < low[p]) low[p] = low[node];
            }
            continue;
        }
        next_arc[node] = edges[arc].next;
        int id = edges[arc].id, next = edges[arc].to;
        if (id == parent_edge[node]) continue;
        if (!entered[next]) {
            parent[next] = node; parent_edge[next] = id;
            entered[next] = low[next] = ++timer;
            next_arc[next] = head[next];
            stack[top++] = next;
        } else if (entered[next] < low[node]) low[node] = entered[next];
    }
    int* answer = calloc(roads_rows, sizeof(*answer));
    int count = 0;
    for (int id = 0; id < m; ++id) if (important[id]) answer[count++] = id + 1;
    if (!count) answer[count++] = -1;
    free(head); free(edges); free(from); free(to); free(heap);
    free(on_path); free(important); free(entered); free(low);
    free(parent); free(parent_edge); free(next_arc); free(stack);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // roads의 행·열 길이를 받을 size_t
// #include <stdlib.h>  // 그래프·최단 거리·반복 DFS 배열의 할당과 해제
// #include <stdbool.h>  // 최단 경로 도로와 정답 도로를 표시할 bool
// #include <limits.h>  // 도달 전 최단 거리에 쓸 큰 long long 값
// 
// typedef struct { int to, next, id; long long weight; } Edge;  // 도착점·인접 목록 연결·원래 도로 번호·통과 시간을 한 간선에 보관
// typedef struct { long long distance; int node; } State;  // 최소 힙에서 비교할 거리와 정점 번호
// 
// static void push(State* heap, int* count, State value) {  // 새 거리 상태를 최소 힙에 넣기
//     int at = ++*count;  // 힙 끝에서 새 상태의 자리를 찾기 시작
//     while (at > 1 && heap[at / 2].distance > value.distance) {  // 부모보다 거리가 작으면 위로 올라가기
//         heap[at] = heap[at / 2];  // 큰 부모를 아래 빈자리로 내리기
//         at /= 2;  // 부모가 있던 위치에서 다시 비교
//     }  // 최소 힙 순서에 맞는 위치 탐색 끝
//     heap[at] = value;  // 찾은 자리에 새 거리 상태 넣기
// }  // 힙 삽입 끝
// 
// static State pop(State* heap, int* count) {  // 거리가 가장 작은 상태를 꺼내기
//     State result = heap[1], value = heap[(*count)--];  // 첫 상태를 보관하고 마지막 상태로 빈자리 메울 준비
//     int at = 1;  // 루트에서 마지막 상태를 내려놓을 위치 찾기
//     while (at * 2 <= *count) {  // 왼쪽 자식이 있는 동안 두 자식과 비교
//         int child = at * 2;  // 우선 왼쪽 자식을 비교 대상으로 선택
//         if (child + 1 <= *count && heap[child + 1].distance < heap[child].distance) ++child;  // 오른쪽 자식이 더 작으면 그쪽 선택
//         if (value.distance <= heap[child].distance) break;  // 마지막 값이 두 자식 이하이면 이 자리에 놓을 수 있음
//         heap[at] = heap[child];  // 작은 자식을 위 빈자리로 올리기
//         at = child;  // 자식의 빈자리에서 계속 비교
//     }  // 마지막 상태를 둘 자리 탐색 끝
//     if (*count) heap[at] = value;  // 힙에 남은 원소가 있을 때만 마지막 상태 기록
//     return result;  // 가장 가까운 미처리 상태 반환
// }  // 힙 최솟값 제거 끝
// 
// static void shortest(int n, int start, const int* head, const Edge* edges, State* heap, long long* distance) {  // 한 출발점에서 모든 정점까지 다익스트라 최단 거리 계산
//     for (int node = 1; node <= n; ++node) distance[node] = LLONG_MAX / 4;  // 아직 도달하지 않은 정점 거리를 충분히 큰 값으로 초기화
//     int count = 0;  // 이번 최단 거리 계산의 힙 원소 수
//     distance[start] = 0;  // 출발점까지 거리는 0
//     push(heap, &count, (State){0, start});  // 출발점을 첫 탐색 상태로 추가
//     while (count) {  // 최소 거리 후보가 남아 있는 동안 탐색
//         State current = pop(heap, &count);  // 가장 작은 거리의 정점 상태 꺼내기
//         if (current.distance != distance[current.node]) continue;  // 더 좋은 경로가 이미 나온 오래된 힙 상태는 제외
//         for (int arc = head[current.node]; arc != -1; arc = edges[arc].next) {  // 현재 정점의 모든 인접 도로 확인
//             int next = edges[arc].to;  // 이번 도로의 이웃 정점
//             long long candidate = current.distance + edges[arc].weight;  // 이 도로를 지난 새 도착 시간
//             if (candidate < distance[next]) {  // 기존 최단 시간보다 작을 때만 갱신
//                 distance[next] = candidate;  // 이웃 정점의 새 최단 시간 저장
//                 push(heap, &count, (State){candidate, next});  // 더 짧아진 상태를 최소 힙에 추가
//             }  // 현재 도로의 거리 완화 끝
//         }  // 현재 정점의 도로 확인 끝
//     }  // 모든 최단 거리 확정
// }  // 한 출발점의 다익스트라 끝
// 
// int* solution(int n, int** roads, size_t roads_rows, size_t roads_cols) {  // 교통량 하나의 변화가 최단 도착 시간을 바꿀 수 있는 도로 번호 찾기
//     (void)roads_cols;  // 각 도로는 U,V,L,T 네 값이므로 열 수는 별도로 쓰지 않음
//     int m = (int)roads_rows;  // 원래 도로 개수
//     int* head = malloc(((size_t)n + 1) * sizeof(*head));  // 정점별 인접 간선 목록의 첫 위치
//     Edge* edges = malloc((size_t)2 * m * sizeof(*edges));  // 양방향 도로를 두 유향 간선으로 저장할 공간
//     for (int node = 1; node <= n; ++node) head[node] = -1;  // 모든 정점의 인접 목록을 빈 상태로 시작
//     for (int id = 0; id < m; ++id) {  // 입력 순서대로 도로를 인접 목록에 등록
//         int u = roads[id][0], v = roads[id][1];  // 이번 도로의 양 끝 정점
//         long long weight = (long long)roads[id][2] + roads[id][3];  // 길이와 교통량을 더한 실제 통과 시간
//         edges[2 * id] = (Edge){v, head[u], id, weight};  // U에서 V로 가는 간선과 기존 U 목록 연결
//         head[u] = 2 * id;  // U의 인접 목록 맨 앞을 새 간선으로 변경
//         edges[2 * id + 1] = (Edge){u, head[v], id, weight};  // V에서 U로 돌아가는 간선도 같은 도로 번호로 등록
//         head[v] = 2 * id + 1;  // V의 인접 목록 맨 앞을 새 간선으로 변경
//     }  // 원래 도로의 양방향 그래프 구성 끝
//     long long* from = malloc(((size_t)n + 1) * sizeof(*from));  // 1번 출발지에서 각 정점까지의 최단 시간
//     long long* to = malloc(((size_t)n + 1) * sizeof(*to));  // 각 정점에서 n번 목적지까지의 최단 시간
//     State* heap = malloc(((size_t)2 * m + 2) * sizeof(*heap));  // 각 유향 간선 완화마다 한 번 들어갈 수 있는 힙 상태 공간
//     shortest(n, 1, head, edges, heap, from);  // 출발지 기준 최단 거리 계산
//     shortest(n, n, head, edges, heap, to);  // 양방향 도로이므로 목적지 기준 거리로 도착까지의 거리 계산
//     long long best = from[n];  // 현재 교통량에서의 가장 빠른 도착 시간
//     bool* on_path = calloc(roads_rows, sizeof(*on_path));  // 현재 최단 경로 중 하나에 들어가는 도로 표시
//     bool* important = calloc(roads_rows, sizeof(*important));  // 교통량 감소 또는 증가로 답을 바꿀 수 있는 도로 표시
//     for (int id = 0; id < m; ++id) {  // 도로별로 감소 가능성과 최단 경로 포함 여부 판정
//         int u = roads[id][0], v = roads[id][1];  // 이번 도로의 양 끝 정점
//         long long length = roads[id][2], weight = length + roads[id][3];  // 교통량 0일 때의 최소 시간과 현재 시간
//         important[id] = from[u] + length + to[v] < best || from[v] + length + to[u] < best;  // 교통량을 0으로 줄여 기존 최단 시간보다 빨라질 수 있는지 양방향 검사
//         on_path[id] = from[u] + weight + to[v] == best || from[v] + weight + to[u] == best;  // 이 도로를 지나는 현재 최단 경로가 하나라도 있는지 표시
//     }  // 교통량 감소에 민감한 도로와 최단 경로 부분 그래프 준비 끝
//     int* entered = calloc((size_t)n + 1, sizeof(*entered));  // 단절선 DFS에서 처음 방문한 순서, 0은 미방문
//     int* low = malloc(((size_t)n + 1) * sizeof(*low));  // 자식과 역방향 간선으로 도달할 수 있는 최소 방문 순서
//     int* parent = calloc((size_t)n + 1, sizeof(*parent));  // 반복 DFS에서 현재 정점의 부모, 루트는 0
//     int* parent_edge = malloc(((size_t)n + 1) * sizeof(*parent_edge));  // 부모에게 연결된 원래 도로 번호
//     int* next_arc = malloc(((size_t)n + 1) * sizeof(*next_arc));  // 각 정점에서 다음에 확인할 인접 간선 위치
//     int* stack = malloc((size_t)n * sizeof(*stack));  // 재귀 대신 DFS 경로를 저장할 스택
//     int top = 0, timer = 1;  // DFS 스택 길이와 방문 순서 번호
//     stack[top++] = 1;  // 출발지에서 최단 경로 부분 그래프 탐색 시작
//     entered[1] = low[1] = timer;  // 출발지의 방문 순서와 최소 도달 순서를 1로 설정
//     parent_edge[1] = -1;  // 출발지에는 부모 도로가 없음
//     next_arc[1] = head[1];  // 출발지에서 첫 번째 인접 도로부터 확인
//     while (top) {  // 반복 DFS로 최단 경로 부분 그래프의 단절선 찾기
//         int node = stack[top - 1];  // 아직 자식 검사가 끝나지 않은 현재 정점
//         int arc = next_arc[node];  // 현재 정점에서 이어서 검사할 도로
//         while (arc != -1 && !on_path[edges[arc].id]) arc = edges[arc].next;  // 현재 최단 경로에 쓰이지 않는 도로는 제외
//         if (arc == -1) {  // 모든 인접 도로 검사를 마쳤으면 부모로 돌아가기
//             --top;  // 현재 정점을 DFS 스택에서 제거
//             int p = parent[node];  // 현재 서브트리 결과를 전달할 부모
//             if (p) {  // 출발지 외 정점에서만 부모 도로를 검사
//                 if (low[node] > entered[p]) important[parent_edge[node]] = true;  // 우회 연결이 없는 단절선은 모든 최단 경로가 지나므로 증가에 민감
//                 if (low[node] < low[p]) low[p] = low[node];  // 자식 쪽에서 도달한 가장 이른 방문 순서를 부모에 반영
//             }  // 부모 도로의 단절선 판정 끝
//             continue;  // 부모 정점의 남은 도로 검사로 복귀
//         }  // 완료 정점을 되돌리는 처리 끝
//         next_arc[node] = edges[arc].next;  // 이 도로를 처리한 뒤 이어서 볼 위치 저장
//         int id = edges[arc].id, next = edges[arc].to;  // 현재 도로의 원래 번호와 이웃 정점
//         if (id == parent_edge[node]) continue;  // 방금 내려온 부모 도로는 역방향 우회로로 세지 않음
//         if (!entered[next]) {  // 처음 만난 이웃이면 DFS 자식으로 내려가기
//             parent[next] = node; parent_edge[next] = id;  // 돌아올 부모 정점과 도로 번호 기록
//             entered[next] = low[next] = ++timer;  // 새 방문 순서를 주고 최소 도달 순서도 같은 값으로 시작
//             next_arc[next] = head[next];  // 자식 정점의 첫 인접 도로부터 검사
//             stack[top++] = next;  // 자식을 DFS 스택에 넣어 그 서브트리부터 처리
//         } else if (entered[next] < low[node]) low[node] = entered[next];  // 이미 본 정점으로의 우회 연결은 최소 도달 순서에 반영
//     }  // 현재 최단 경로를 모두 지나는 도로 표시 끝
//     int* answer = calloc(roads_rows, sizeof(*answer));  // 최대 m개 도로 번호의 반환 공간을 0으로 초기화
//     int count = 0;  // 찾은 중요한 도로 개수
//     for (int id = 0; id < m; ++id) if (important[id]) answer[count++] = id + 1;  // 원래 도로 번호를 작은 순서대로 결과에 추가
//     if (!count) answer[count++] = -1;  // 교통량 변화에 민감한 도로가 없으면 -1 한 개 반환
//     free(head); free(edges); free(from); free(to); free(heap);  // 원래 그래프와 두 번의 최단 거리 계산 공간 해제
//     free(on_path); free(important); free(entered); free(low);  // 최단 경로 표시와 단절선 방문 배열 해제
//     free(parent); free(parent_edge); free(next_arc); free(stack);  // 재귀 대신 쓴 DFS 상태 배열 해제
//     return answer;  // 오름차순 도로 번호 배열 반환
// }  // 중요한 도로 계산 끝

// 풀이 요약
// 1번과 n번에서 다익스트라를 한 번씩 실행해 현재 최단 시간 D와 양끝 거리 계산
// 교통량을 0으로 내렸을 때 dist1[u]+L+distN[v] 또는 반대 방향이 D보다 작으면 감소에 민감한 도로
// 현재 최단 경로에 속하는 도로만 모은 부분 그래프에서 단절선을 찾으면 증가에 민감한 도로
// 모든 부분 그래프 도로는 실제 최단 경로에 들어가고 길이가 양수이므로, 단절선과 모든 최단 경로가 지나는 도로가 일치
// 두 조건 중 하나라도 만족하는 도로 번호를 오름차순으로 반환하고 없으면 [-1]
// 거리 합은 long long, DFS는 반복 스택 사용; 정점 N·도로 M에 대해 시간 O((N+M) log N), 공간 O(N+M)
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
