# 홀짝트리

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/388354) · Level 3 · C

## 풀이

루트의 자식 수는 차수와 같고, 나머지 노드의 자식 수는 차수-1이라 홀짝이 뒤집힘

따라서 번호·차수 홀짝 일치 노드가 정확히 하나면 홀짝 트리, 불일치가 정확히 하나면 역홀짝 트리; 서로소 집합으로 트리를 묶어 개수만 세기; 시간 O((N+E)α(N)), 공간 O(N); α는 매우 느리게 증가하는 역 아커만 함수

예: 고립된 짝수 노드는 자식 0개이므로 홀짝 트리, 고립된 홀수 노드는 역홀짝 트리; 루트 선택 수가 아니라 가능한 트리 수를 세기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int label, index; } Node;
static int compare(const void* p, const void* q) { int a = ((const Node*)p)->label, b = ((const Node*)q)->label; return (a > b) - (a < b); }
static int lookup(const Node* nodes, size_t n, int value) { size_t low = 0, high = n; while (low < high) { size_t mid = (low + high) / 2; if (nodes[mid].label < value) low = mid + 1; else high = mid; } return nodes[low].index; }
static int find(int* parent, int node) { while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; } return node; }
int* solution(int nodes[], size_t nodes_len, int** edges, size_t edges_rows, size_t edges_cols) {
    (void)edges_cols; Node* sorted = malloc(nodes_len * sizeof(*sorted)); int* parent = malloc(nodes_len * sizeof(*parent)); int* size = malloc(nodes_len * sizeof(*size));
    int* degree = calloc(nodes_len, sizeof(*degree)); int* matches = calloc(nodes_len, sizeof(*matches));
    for (size_t i = 0; i < nodes_len; ++i) { sorted[i] = (Node){nodes[i],(int)i}; parent[i] = (int)i; size[i] = 1; } qsort(sorted, nodes_len, sizeof(*sorted), compare);
    for (size_t i = 0; i < edges_rows; ++i) {
        int a = lookup(sorted, nodes_len, edges[i][0]), b = lookup(sorted, nodes_len, edges[i][1]); ++degree[a]; ++degree[b];
        a = find(parent,a); b = find(parent,b); if (a != b) { if (size[a] < size[b]) { int temp = a; a = b; b = temp; } parent[b] = a; size[a] += size[b]; }
    }
    for (size_t i = 0; i < nodes_len; ++i) if (nodes[i] % 2 == degree[i] % 2) ++matches[find(parent,(int)i)];
    int* answer = calloc(2, sizeof(*answer)); for (size_t i = 0; i < nodes_len; ++i) if (parent[i] == (int)i) { answer[0] += matches[i] == 1; answer[1] += matches[i] == size[i] - 1; }
    free(sorted); free(parent); free(size); free(degree); free(matches);
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
// typedef struct { int label, index; } Node;  // 정렬할 레이블과 입력에서의 원래 번호를 함께 보관
// static int compare(const void* p, const void* q) { int a = ((const Node*)p)->label, b = ((const Node*)q)->label; return (a > b) - (a < b); }  // 노드 레이블을 작은 값부터 정렬
// static int lookup(const Node* nodes, size_t n, int value) { size_t low = 0, high = n; while (low < high) { size_t mid = (low + high) / 2; if (nodes[mid].label < value) low = mid + 1; else high = mid; } return nodes[low].index; }  // 이름 또는 레이블에 대응하는 원래 번호 찾기
// static int find(int* parent, int node) { while (parent[node] != node) { parent[node] = parent[parent[node]]; node = parent[node]; } return node; }  // 부모를 따라가며 연결 성분 대표 찾기
// int* solution(int nodes[], size_t nodes_len, int** edges, size_t edges_rows, size_t edges_cols) {  // 루트의 자식 수는 차수와 같고, 나머지 노드의 자식 수는 차수-1이라 홀짝이 뒤집힘
//     (void)edges_cols; Node* sorted = malloc(nodes_len * sizeof(*sorted)); int* parent = malloc(nodes_len * sizeof(*parent)); int* size = malloc(nodes_len * sizeof(*size));  // 레이블순 노드와 원래 인덱스 / 연결 집합 대표 / 컴포넌트 노드 수 공간 확보
//     int* degree = calloc(nodes_len, sizeof(*degree)); int* matches = calloc(nodes_len, sizeof(*matches));  // 노드별 간선 수 / 레이블과 차수의 짝홀이 같은 노드 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < nodes_len; ++i) { sorted[i] = (Node){nodes[i],(int)i}; parent[i] = (int)i; size[i] = 1; } qsort(sorted, nodes_len, sizeof(*sorted), compare);  // 노드 또는 간선 위치 순서대로 확인; 레이블순 노드와 원래 인덱스 / 노드 또는 간선 위치 정렬 순서 맞추기
//     for (size_t i = 0; i < edges_rows; ++i) {  // 노드 또는 간선 위치 순서대로 확인
//         int a = lookup(sorted, nodes_len, edges[i][0]), b = lookup(sorted, nodes_len, edges[i][1]); ++degree[a]; ++degree[b];  // 첫 노드의 번호 또는 대표 / 둘째 노드의 번호 또는 대표 저장
//         a = find(parent,a); b = find(parent,b); if (a != b) { if (size[a] < size[b]) { int temp = a; a = b; b = temp; } parent[b] = a; size[a] += size[b]; }  // 첫 노드의 번호 또는 대표 / 둘째 노드의 번호 또는 대표 / 연결 집합 대표 갱신
//     }  // 이 범위 끝
//     for (size_t i = 0; i < nodes_len; ++i) if (nodes[i] % 2 == degree[i] % 2) ++matches[find(parent,(int)i)];  // 번호와 차수의 홀짝이 같은 노드 수를 연결 성분별로 세기
//     int* answer = calloc(2, sizeof(*answer)); for (size_t i = 0; i < nodes_len; ++i) if (parent[i] == (int)i) { answer[0] += matches[i] == 1; answer[1] += matches[i] == size[i] - 1; }  // 홀짝트리와 역홀짝트리의 개수 / 노드 또는 간선 위치 공간 확보하고 0으로 시작
//     free(sorted); free(parent); free(size); free(degree); free(matches);  // 레이블순 노드와 원래 인덱스 / 연결 집합 대표 / 컴포넌트 노드 수 / 노드별 간선 수 임시 공간 정리
//     return answer;  // 홀짝트리와 역홀짝트리의 개수 반환
// }  // 이 범위 끝

// 풀이 요약
// 루트의 자식 수는 차수와 같고, 나머지 노드의 자식 수는 차수-1이라 홀짝이 뒤집힘
// 따라서 번호·차수 홀짝 일치 노드가 정확히 하나면 홀짝 트리, 불일치가 정확히 하나면 역홀짝 트리; 서로소 집합으로 트리를 묶어 개수만 세기; 시간 O((N+E)α(N)), 공간 O(N); α는 매우 느리게 증가하는 역 아커만 함수
// 예: 고립된 짝수 노드는 자식 0개이므로 홀짝 트리, 고립된 홀수 노드는 역홀짝 트리; 루트 선택 수가 아니라 가능한 트리 수를 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:26:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/009_388354_%ED%99%80%EC%A7%9D%ED%8A%B8%EB%A6%AC/README.md)
