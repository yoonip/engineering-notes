#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

long long solution(int a[], size_t a_len, int** edges, size_t edges_rows, size_t edges_cols) {
    (void)edges_cols; long long total = 0;
    for (size_t i = 0; i < a_len; ++i) total += a[i];
    if (total) return -1;
    int* head = malloc(a_len * sizeof(*head)); int* next = malloc(2 * edges_rows * sizeof(*next)); int* to = malloc(2 * edges_rows * sizeof(*to));
    for (size_t i = 0; i < a_len; ++i) head[i] = -1;
    int count = 0;
    for (size_t i = 0; i < edges_rows; ++i) for (int d = 0; d < 2; ++d) { int u = edges[i][d], v = edges[i][1 - d]; to[count] = v; next[count] = head[u]; head[u] = count++; }
    int* parent = malloc(a_len * sizeof(*parent)); int* order = malloc(a_len * sizeof(*order)); long long* weight = malloc(a_len * sizeof(*weight));
    for (size_t i = 0; i < a_len; ++i) { parent[i] = -1; weight[i] = a[i]; }
    size_t tail = 1; order[0] = 0;
    for (size_t i = 0; i < tail; ++i) for (int e = head[order[i]]; e >= 0; e = next[e]) if (to[e] != parent[order[i]]) { parent[to[e]] = order[i]; order[tail++] = to[e]; }
    long long answer = 0;
    for (size_t i = tail; i-- > 1;) { int node = order[i]; answer += llabs(weight[node]); weight[parent[node]] += weight[node]; }
    free(head); free(next); free(to); free(parent); free(order); free(weight);
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
// long long solution(int a[], size_t a_len, int** edges, size_t edges_rows, size_t edges_cols) {  // 전체 가중치 합이 0일 때만 가능하다; 잎부터 가중치를 부모에게 넘기고 넘긴 양의 절댓값을 더하기
//     (void)edges_cols; long long total = 0;  // 처음 가중치 총합 갱신
//     for (size_t i = 0; i < a_len; ++i) total += a[i];  // 노드 또는 간선 위치 순서대로 확인; 처음 가중치 총합 / 노드 또는 간선 위치 더해 누적
//     if (total) return -1;  // 처음 가중치 총합가 남아 있으면 조건에 맞는 답이 없으면 -1
//     int* head = malloc(a_len * sizeof(*head)); int* next = malloc(2 * edges_rows * sizeof(*next)); int* to = malloc(2 * edges_rows * sizeof(*to));  // 노드별 첫 간선 / 인접 리스트의 다음 간선 / 간선의 도착 노드 공간 확보
//     for (size_t i = 0; i < a_len; ++i) head[i] = -1;  // 노드 또는 간선 위치 순서대로 확인; 노드별 첫 간선 갱신
//     int count = 0;  // 채운 양방향 간선 수 저장
//     for (size_t i = 0; i < edges_rows; ++i) for (int d = 0; d < 2; ++d) { int u = edges[i][d], v = edges[i][1 - d]; to[count] = v; next[count] = head[u]; head[u] = count++; }  // 노드 또는 간선 위치 순서대로 확인; 간선 방향 / 채운 양방향 간선 수 갱신
//     int* parent = malloc(a_len * sizeof(*parent)); int* order = malloc(a_len * sizeof(*order)); long long* weight = malloc(a_len * sizeof(*weight));  // 루트 기준 부모 / 부모가 먼저 오는 탐색 순서 / 자식 값을 합친 현재 가중치 공간 확보
//     for (size_t i = 0; i < a_len; ++i) { parent[i] = -1; weight[i] = a[i]; }  // 노드 또는 간선 위치 순서대로 확인; 루트 기준 부모 / 자식 값을 합친 현재 가중치 갱신
//     size_t tail = 1; order[0] = 0;  // 탐색한 노드 수 / 부모가 먼저 오는 탐색 순서 저장
//     for (size_t i = 0; i < tail; ++i) for (int e = head[order[i]]; e >= 0; e = next[e]) if (to[e] != parent[order[i]]) { parent[to[e]] = order[i]; order[tail++] = to[e]; }  // 노드 또는 간선 위치 순서대로 확인; 탐색한 노드 수 갱신
//     long long answer = 0;  // 옮긴 가중치 절댓값 합 저장
//     for (size_t i = tail; i-- > 1;) { int node = order[i]; answer += llabs(weight[node]); weight[parent[node]] += weight[node]; }  // 노드 또는 간선 위치 순서대로 확인; 가중치를 부모로 넘길 노드 저장
//     free(head); free(next); free(to); free(parent); free(order); free(weight);  // 노드별 첫 간선 / 인접 리스트의 다음 간선 / 간선의 도착 노드 / 루트 기준 부모 임시 공간 정리
//     return answer;  // 옮긴 가중치 절댓값 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 전체 가중치 합이 0일 때만 가능하다; 잎부터 가중치를 부모에게 넘기고 넘긴 양의 절댓값을 더하기
// 예: [-5,0,2,1,2]에서는 두 잎의 2씩과 가운데 누적 5를 옮겨 2+2+5=9번
// 트리의 간선을 끊으면 부분 트리의 합만큼 반드시 그 간선을 지나야 하므로 이 횟수가 최소; 시간·공간 O(N)
