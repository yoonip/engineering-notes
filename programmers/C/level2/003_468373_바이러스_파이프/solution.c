#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int find(int* parent, int node) {
    while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; }
    return node;
}
static void search(const int* groups, int n, const bool* infected, int remaining, int* answer) {
    int count = 0;
    for (int i = 0; i < n; ++i) count += infected[i];
    if (count > *answer) *answer = count;
    if (!remaining || *answer == n) return;
    bool* marked = calloc((size_t)n, sizeof(*marked)); bool* next = malloc((size_t)n * sizeof(*next));
    for (int kind = 0; kind < 3; ++kind) {
        memset(marked, 0, (size_t)n * sizeof(*marked));
        for (int i = 0; i < n; ++i) if (infected[i]) marked[groups[kind * n + i]] = true;
        bool changed = false;
        for (int i = 0; i < n; ++i) { next[i] = marked[groups[kind * n + i]]; changed |= next[i] != infected[i]; }
        if (changed) search(groups, n, next, remaining - 1, answer);
    }
    free(marked); free(next);
}
int solution(int n, int infection, int** edges, size_t edges_rows, size_t edges_cols, int k) {
    (void)edges_cols;
    int* groups = malloc((size_t)3 * n * sizeof(*groups));
    for (int kind = 0; kind < 3; ++kind) for (int i = 0; i < n; ++i) groups[kind * n + i] = i;
    for (size_t i = 0; i < edges_rows; ++i) {
        int* parent = groups + (edges[i][2] - 1) * n;
        int a = find(parent, edges[i][0] - 1), b = find(parent, edges[i][1] - 1); parent[a] = b;
    }
    for (int kind = 0; kind < 3; ++kind) for (int i = 0; i < n; ++i) groups[kind * n + i] = find(groups + kind * n, i);
    bool* infected = calloc((size_t)n, sizeof(*infected)); infected[infection - 1] = true; int answer = 1;
    search(groups, n, infected, k, &answer); free(groups); free(infected);
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
// static int find(int* parent, int node) {  // 부모를 따라가며 연결 성분 대표 찾기
//     while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; }  // 루트까지 올라가며 조부모로 연결해서 다음 탐색 경로 압축
//     return node;  // 대표를 찾는 노드 반환
// }  // 이 범위 끝
// static void search(const int* groups, int n, const bool* infected, int remaining, int* answer) {  // 종류별 노드의 연결 성분 / 현재 감염된 노드 표시 / 앞으로 열 수 있는 횟수 / 가능한 최대 감염 노드 수 계산용 함수
//     int count = 0;  // 감염된 노드 수 저장
//     for (int i = 0; i < n; ++i) count += infected[i];  // 노드 또는 간선 번호 순서대로 확인; 감염된 노드 수 / 현재 감염된 노드 표시 / 노드 또는 간선 번호 더해 누적
//     if (count > *answer) *answer = count;  // 이번 선택이 지금까지의 최댓값보다 크면 가능한 최대 감염 노드 수 갱신
//     if (!remaining || *answer == n) return;  // 열 수 있는 횟수가 없거나 모든 노드가 감염됐으면 탐색 종료
//     bool* marked = calloc((size_t)n, sizeof(*marked)); bool* next = malloc((size_t)n * sizeof(*next));  // 감염원이 있는 연결 성분 / 같은 종류를 한 번 열었을 때 감염 표시 공간 확보하고 0으로 시작
//     for (int kind = 0; kind < 3; ++kind) {  // 이번에 열 파이프 종류 순서대로 확인
//         memset(marked, 0, (size_t)n * sizeof(*marked));  // 감염원이 있는 연결 성분 초기화
//         for (int i = 0; i < n; ++i) if (infected[i]) marked[groups[kind * n + i]] = true;  // 감염 노드가 들어 있는 연결 성분을 표시
//         bool changed = false;  // 새 감염이 생겼는지 여부 저장
//         for (int i = 0; i < n; ++i) { next[i] = marked[groups[kind * n + i]]; changed |= next[i] != infected[i]; }  // 노드 또는 간선 번호 순서대로 확인; 같은 종류를 한 번 열었을 때 감염 표시 갱신
//         if (changed) search(groups, n, next, remaining - 1, answer);  // 새로 감염된 노드가 있을 때만 남은 개방 횟수를 줄여 다음 선택 탐색
//     }  // 이 범위 끝
//     free(marked); free(next);  // 감염원이 있는 연결 성분 / 같은 종류를 한 번 열었을 때 감염 표시 임시 공간 정리
// }  // 이 범위 끝
// int solution(int n, int infection, int** edges, size_t edges_rows, size_t edges_cols, int k) {  // 파이프 종류별 연결 성분을 서로소 집합으로 구하고 각 노드의 대표 번호를 배열에 저장
//     (void)edges_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* groups = malloc((size_t)3 * n * sizeof(*groups));  // 종류별 노드의 연결 성분 공간 확보
//     for (int kind = 0; kind < 3; ++kind) for (int i = 0; i < n; ++i) groups[kind * n + i] = i;  // 이번에 열 파이프 종류 순서대로 확인; 노드 또는 간선 번호 갱신
//     for (size_t i = 0; i < edges_rows; ++i) {  // 노드 또는 간선 번호 순서대로 확인
//         int* parent = groups + (edges[i][2] - 1) * n;  // 파이프 종류별 연결 집합 부모 저장
//         int a = find(parent, edges[i][0] - 1), b = find(parent, edges[i][1] - 1); parent[a] = b;  // 첫 노드의 대표 / 둘째 노드의 대표 / 파이프 종류별 연결 집합 부모 저장
//     }  // 이 범위 끝
//     for (int kind = 0; kind < 3; ++kind) for (int i = 0; i < n; ++i) groups[kind * n + i] = find(groups + kind * n, i);  // 이번에 열 파이프 종류 순서대로 확인; 노드 또는 간선 번호 갱신
//     bool* infected = calloc((size_t)n, sizeof(*infected)); infected[infection - 1] = true; int answer = 1;  // 현재 감염된 노드 표시 / 가능한 최대 감염 노드 수 공간 확보하고 0으로 시작
//     search(groups, n, infected, k, &answer); free(groups); free(infected);  // 종류별 노드의 연결 성분 / 현재 감염된 노드 표시 / 가능한 최대 감염 노드 수 임시 공간 정리
//     return answer;  // 가능한 최대 감염 노드 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 파이프 종류별 연결 성분을 서로소 집합으로 구하고 각 노드의 대표 번호를 배열에 저장
// 한 종류를 선택하면 감염 정점과 닿은 연결 요소 전체가 감염됨; 최대 k번의 선택을 DFS로 비교
// 예: 감염 집합 {1}, 선택한 종류의 연결 요소 {1,2,3}이면 다음 감염 집합은 {1,2,3}
