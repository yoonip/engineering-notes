#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int to, cost, next; bool reverse; } Edge;
typedef struct { long long cost; int node; unsigned mask; } State;
typedef struct { State* items; size_t count, capacity; } Heap;
static void push(Heap* heap, State value) {
    if (heap->count == heap->capacity) { heap->capacity *= 2; heap->items = realloc(heap->items,heap->capacity * sizeof(*heap->items)); }
    size_t at = heap->count++;
    while (at && heap->items[(at - 1) / 2].cost > value.cost) { heap->items[at] = heap->items[(at - 1) / 2]; at = (at - 1) / 2; }
    heap->items[at] = value;
}
static State pop(Heap* heap) {
    State result = heap->items[0], value = heap->items[--heap->count]; size_t at = 0;
    while (at * 2 + 1 < heap->count) {
        size_t child = at * 2 + 1; if (child + 1 < heap->count && heap->items[child + 1].cost < heap->items[child].cost) ++child;
        if (heap->items[child].cost >= value.cost) break; heap->items[at] = heap->items[child]; at = child;
    }
    if (heap->count) heap->items[at] = value;
    return result;
}
int solution(int n, int start, int end, int** roads, size_t roads_rows, size_t roads_cols, int traps[], size_t traps_len) {
    (void)roads_cols; size_t states = (size_t)1 << traps_len;
    unsigned* bits = calloc((size_t)n + 1,sizeof(*bits)); for (size_t i = 0; i < traps_len; ++i) bits[traps[i]] = 1u << i;
    int* head = malloc(((size_t)n + 1) * sizeof(*head)); for (int i = 0; i <= n; ++i) head[i] = -1;
    Edge* edges = malloc(2 * roads_rows * sizeof(*edges)); int count = 0;
    for (size_t i = 0; i < roads_rows; ++i) for (int d = 0; d < 2; ++d) { int a = roads[i][d], b = roads[i][1 - d]; edges[count] = (Edge){b,roads[i][2],head[a],d != 0}; head[a] = count++; }
    long long* distance = malloc(((size_t)n + 1) * states * sizeof(*distance)); for (size_t i = 0; i < ((size_t)n + 1) * states; ++i) distance[i] = LLONG_MAX;
    Heap heap = {malloc(1024 * sizeof(State)),0,1024}; distance[(size_t)start * states] = 0; push(&heap,(State){0,start,0}); int answer = -1;
    while (heap.count) {
        State current = pop(&heap); if (current.cost != distance[(size_t)current.node * states + current.mask]) continue;
        if (current.node == end) { answer = (int)current.cost; break; }
        bool active = (current.mask & bits[current.node]) != 0;
        for (int e = head[current.node]; e >= 0; e = edges[e].next) {
            Edge edge = edges[e]; bool flipped = active != ((current.mask & bits[edge.to]) != 0); if (flipped != edge.reverse) continue;
            unsigned mask = current.mask ^ bits[edge.to]; long long cost = current.cost + edge.cost; size_t index = (size_t)edge.to * states + mask;
            if (cost < distance[index]) { distance[index] = cost; push(&heap,(State){cost,edge.to,mask}); }
        }
    }
    free(bits); free(head); free(edges); free(distance); free(heap.items);
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
// typedef struct { int to, cost, next; bool reverse; } Edge;  // 다음 도로까지의 누적 비용를 한 상태로 묶기
// typedef struct { long long cost; int node; unsigned mask; } State;  // 다음 도로까지의 누적 비용 / 다음 칸에 들어간 뒤 함정 상태를 한 상태로 묶기
// typedef struct { State* items; size_t count, capacity; } Heap;  // 저장한 방향 간선 수를 한 상태로 묶기
// static void push(Heap* heap, State value) {  // 새 상태를 힙에 넣고 부모 방향으로 자리 찾기
//     if (heap->count == heap->capacity) { heap->capacity *= 2; heap->items = realloc(heap->items,heap->capacity * sizeof(*heap->items)); }  // 힙이 꽉 찼으면 저장 공간을 두 배로 늘리기
//     size_t at = heap->count++;  // 힙에서 재배치할 위치 저장
//     while (at && heap->items[(at - 1) / 2].cost > value.cost) { heap->items[at] = heap->items[(at - 1) / 2]; at = (at - 1) / 2; }  // 힙에 미처리 상태가 남아 있는 동안 우선순위가 가장 높은 상태를 처리
//     heap->items[at] = value;  // 힙에서 재배치할 위치 / 힙에 내려놓을 상태 확인
// }  // 이 범위 끝
// static State pop(Heap* heap) {  // 힙의 첫 값을 꺼내고 마지막 값으로 빈자리 메우기
//     State result = heap->items[0], value = heap->items[--heap->count]; size_t at = 0;  // 힙에서 꺼낸 최소 비용 상태 / 힙에 내려놓을 상태 / 힙에서 재배치할 위치 저장
//     while (at * 2 + 1 < heap->count) {  // 힙에 미처리 상태가 남아 있는 동안 우선순위가 가장 높은 상태를 처리
//         size_t child = at * 2 + 1; if (child + 1 < heap->count && heap->items[child + 1].cost < heap->items[child].cost) ++child;  // 비용이 더 작은 자식을 골라 힙의 아래 빈자리 찾기
//         if (heap->items[child].cost >= value.cost) break; heap->items[at] = heap->items[child]; at = child;  // 부모와 자식의 힙 순서가 이미 맞으면 이번 후보 확인을 끝내기
//     }  // 이 범위 끝
//     if (heap->count) heap->items[at] = value;  // 꺼낸 뒤 힙이 남아 있으면 마지막 값을 찾은 자리에 넣기
//     return result;  // 힙에서 꺼낸 최소 비용 상태 반환
// }  // 이 범위 끝
// int solution(int n, int start, int end, int** roads, size_t roads_rows, size_t roads_cols, int traps[], size_t traps_len) {  // 방 번호만으로 방문 처리하면 안 됨; 같은 방도 함정 활성 조합이 다르면 다른 상태로 보고 다익스트라 최단 경로를 계산
//     (void)roads_cols; size_t states = (size_t)1 << traps_len;  // 함정 활성 조합 수 비트 상태 갱신
//     unsigned* bits = calloc((size_t)n + 1,sizeof(*bits)); for (size_t i = 0; i < traps_len; ++i) bits[traps[i]] = 1u << i;  // 노드별 함정 비트 / 함정 또는 거리 초기화 위치 공간 확보하고 0으로 시작
//     int* head = malloc(((size_t)n + 1) * sizeof(*head)); for (int i = 0; i <= n; ++i) head[i] = -1;  // 노드별 첫 원래 또는 역방향 간선 / 함정 또는 거리 초기화 위치 공간 확보
//     Edge* edges = malloc(2 * roads_rows * sizeof(*edges)); int count = 0;  // 원래 방향 표시를 포함한 간선 / 저장한 방향 간선 수 공간 확보
//     for (size_t i = 0; i < roads_rows; ++i) for (int d = 0; d < 2; ++d) { int a = roads[i][d], b = roads[i][1 - d]; edges[count] = (Edge){b,roads[i][2],head[a],d != 0}; head[a] = count++; }  // 함정 또는 거리 초기화 위치 순서대로 확인; 원래 또는 역방향 / 저장한 방향 간선 수 갱신
//     long long* distance = malloc(((size_t)n + 1) * states * sizeof(*distance)); for (size_t i = 0; i < ((size_t)n + 1) * states; ++i) distance[i] = LLONG_MAX;  // 노드와 함정 상태별 최단 비용 / 함정 또는 거리 초기화 위치 공간 확보
//     Heap heap = {malloc(1024 * sizeof(State)),0,1024}; distance[(size_t)start * states] = 0; push(&heap,(State){0,start,0}); int answer = -1;  // 가장 싼 상태를 꺼낼 최소 힙 / 노드와 함정 상태별 최단 비용 / 함정 방향을 반영한 출구 최단 비용 공간 확보
//     while (heap.count) {  // 힙에 미처리 상태가 남아 있는 동안 우선순위가 가장 높은 상태를 처리
//         State current = pop(&heap); if (current.cost != distance[(size_t)current.node * states + current.mask]) continue;  // 최소 비용 상태를 꺼내고 더 좋은 거리가 이미 있으면 건너뛰기
//         if (current.node == end) { answer = (int)current.cost; break; }  // 도착 노드를 꺼냈으면 현재 비용이 최단 비용이므로 종료
//         bool active = (current.mask & bits[current.node]) != 0;  // 현재 노드의 함정 활성 여부 저장
//         for (int e = head[current.node]; e >= 0; e = edges[e].next) {  // 현재 간선 위치 순서대로 확인
//             Edge edge = edges[e]; bool flipped = active != ((current.mask & bits[edge.to]) != 0); if (flipped != edge.reverse) continue;  // 양끝 함정 활성 상태가 다르면 뒤집힌 방향만 통과 가능
//             unsigned mask = current.mask ^ bits[edge.to]; long long cost = current.cost + edge.cost; size_t index = (size_t)edge.to * states + mask;  // 다음 칸에 들어간 뒤 함정 상태 / 다음 도로까지의 누적 비용 / 다음 상태의 거리 배열 위치 저장
//             if (cost < distance[index]) { distance[index] = cost; push(&heap,(State){cost,edge.to,mask}); }  // 이번 경로가 저장된 최단 거리보다 짧으면 다음에 확인할 경로를 힙에 추가
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(bits); free(head); free(edges); free(distance); free(heap.items);  // 노드별 함정 비트 / 노드별 첫 원래 또는 역방향 간선 / 원래 방향 표시를 포함한 간선 / 노드와 함정 상태별 최단 비용 임시 공간 정리
//     return answer;  // 함정 방향을 반영한 출구 최단 비용 반환
// }  // 이 범위 끝

// 풀이 요약
// 방 번호만으로 방문 처리하면 안 됨; 같은 방도 함정 활성 조합이 다르면 다른 상태로 보고 다익스트라 최단 경로를 계산
// 통로 양 끝 함정 중 하나만 활성일 때 역방향; 예제 2처럼 1→2→3→2→4 재방문이 필요할 수 있음
// 함정 수 T, 통로 수 E일 때 시간 O((n+E)*2^T*log(n*2^T)), 공간 O(n*2^T+E)
