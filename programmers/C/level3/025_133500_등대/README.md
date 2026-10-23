# 등대

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/133500) · Level 3 · C

## 풀이

모든 뱃길을 덮는 트리의 최소 정점 커버 문제; 각 노드를 켜는 경우·끄는 경우의 최소 비용을 따로 두기
부모가 꺼져 있으면 자식은 켜야 하고, 부모가 켜져 있으면 자식 두 상태 중 싼 쪽을 택하기; 방문 순서를 뒤집어 재귀 깊이 문제 없이 계산; 시간·공간 O(N)
예: 첫 예제에서 1번을 켜면 2·3·4번은 꺼도 되고, 5번을 켜면 6·7·8번도 꺼도 됨; 총 2개

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int n, int** lighthouse, size_t lighthouse_rows, size_t lighthouse_cols) {
    (void)lighthouse_cols;
    int* head = malloc(((size_t)n + 1) * sizeof(*head)); int* to = malloc(2 * lighthouse_rows * sizeof(*to)); int* next = malloc(2 * lighthouse_rows * sizeof(*next));
    int* parent = calloc((size_t)n + 1, sizeof(*parent)); int* order = malloc((size_t)n * sizeof(*order)); int* off = calloc((size_t)n + 1, sizeof(*off)); int* on = malloc(((size_t)n + 1) * sizeof(*on));
    for (int i = 0; i <= n; ++i) { head[i] = -1; on[i] = 1; }
    int count = 0;
    for (size_t i = 0; i < lighthouse_rows; ++i) for (int d = 0; d < 2; ++d) { int a = lighthouse[i][d], b = lighthouse[i][1 - d]; to[count] = b; next[count] = head[a]; head[a] = count++; }
    int tail = 1; order[0] = 1;
    for (int i = 0; i < tail; ++i) for (int e = head[order[i]]; e >= 0; e = next[e]) if (to[e] != parent[order[i]]) { parent[to[e]] = order[i]; order[tail++] = to[e]; }
    for (int i = tail - 1; i > 0; --i) { int node = order[i], p = parent[node]; off[p] += on[node]; on[p] += off[node] < on[node] ? off[node] : on[node]; }
    int answer = off[1] < on[1] ? off[1] : on[1]; free(head); free(to); free(next); free(parent); free(order); free(off); free(on);
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
// int solution(int n, int** lighthouse, size_t lighthouse_rows, size_t lighthouse_cols) {  // 모든 뱃길을 덮는 트리의 최소 정점 커버 문제; 각 노드를 켜는 경우·끄는 경우의 최소 비용을 따로 두기
//     (void)lighthouse_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* head = malloc(((size_t)n + 1) * sizeof(*head)); int* to = malloc(2 * lighthouse_rows * sizeof(*to)); int* next = malloc(2 * lighthouse_rows * sizeof(*next));  // 등대별 첫 연결 / 연결 상대 등대 / 같은 등대의 다음 간선 공간 확보
//     int* parent = calloc((size_t)n + 1, sizeof(*parent)); int* order = malloc((size_t)n * sizeof(*order)); int* off = calloc((size_t)n + 1, sizeof(*off)); int* on = malloc(((size_t)n + 1) * sizeof(*on));  // 루트 기준 부모 등대 / 부모가 앞선 탐색 순서 / 현재 등대를 끈 서브트리 최소 점등 수 / 현재 등대를 켠 서브트리 최소 점등 수 공간 확보하고 0으로 시작
//     for (int i = 0; i <= n; ++i) { head[i] = -1; on[i] = 1; }  // 노드 또는 간선 위치 순서대로 확인; 등대별 첫 연결 / 현재 등대를 켠 서브트리 최소 점등 수 갱신
//     int count = 0;  // 저장한 방향 간선 수 저장
//     for (size_t i = 0; i < lighthouse_rows; ++i) for (int d = 0; d < 2; ++d) { int a = lighthouse[i][d], b = lighthouse[i][1 - d]; to[count] = b; next[count] = head[a]; head[a] = count++; }  // 노드 또는 간선 위치 순서대로 확인; 양방향 방향 / 저장한 방향 간선 수 갱신
//     int tail = 1; order[0] = 1;  // 탐색 순서 길이 / 부모가 앞선 탐색 순서 저장
//     for (int i = 0; i < tail; ++i) for (int e = head[order[i]]; e >= 0; e = next[e]) if (to[e] != parent[order[i]]) { parent[to[e]] = order[i]; order[tail++] = to[e]; }  // 노드 또는 간선 위치 순서대로 확인; 탐색 순서 길이 갱신
//     for (int i = tail - 1; i > 0; --i) { int node = order[i], p = parent[node]; off[p] += on[node]; on[p] += off[node] < on[node] ? off[node] : on[node]; }  // 노드 또는 간선 위치 순서대로 확인; 자식 결과를 합칠 등대 / 부모 등대 저장
//     int answer = off[1] < on[1] ? off[1] : on[1]; free(head); free(to); free(next); free(parent); free(order); free(off); free(on);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 모든 뱃길을 비추는 최소 등대 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 모든 뱃길을 덮는 트리의 최소 정점 커버 문제; 각 노드를 켜는 경우·끄는 경우의 최소 비용을 따로 두기
// 부모가 꺼져 있으면 자식은 켜야 하고, 부모가 켜져 있으면 자식 두 상태 중 싼 쪽을 택하기; 방문 순서를 뒤집어 재귀 깊이 문제 없이 계산; 시간·공간 O(N)
// 예: 첫 예제에서 1번을 켜면 2·3·4번은 꺼도 되고, 5번을 켜면 6·7·8번도 꺼도 됨; 총 2개
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/025_133500_%EB%93%B1%EB%8C%80/README.md)
