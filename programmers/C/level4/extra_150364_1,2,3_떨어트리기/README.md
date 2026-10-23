# 1,2,3 떨어트리기

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150364) · Level 4 · C

## 풀이

공의 값은 도착 리프에 영향을 주지 않음; 리프마다 공 개수 c에 대해 c≤target≤3c가 처음 모두 성립할 때 멈추기
이후 앞자리부터 가능한 가장 작은 값을 선택; 예: 목표 7에 공 3개면 [1,3,3]으로 배정하기
공 수를 B, 트리 높이를 H라 하면 시간 O(B*H+n*log n), 공간 O(B+n)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static int compare(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }
int* solution(int** edges, size_t edges_rows, size_t edges_cols, int target[], size_t target_len) {
    (void)edges_cols; size_t n = target_len; int* degree = calloc(n,sizeof(*degree)); size_t* start = calloc(n + 1,sizeof(*start));
    for (size_t i = 0; i < edges_rows; ++i) ++degree[edges[i][0] - 1];
    for (size_t i = 0; i < n; ++i) start[i + 1] = start[i] + degree[i];
    int* children = malloc(edges_rows * sizeof(*children)); size_t* cursor = malloc(n * sizeof(*cursor)); memcpy(cursor,start,n * sizeof(*cursor));
    for (size_t i = 0; i < edges_rows; ++i) children[cursor[edges[i][0] - 1]++] = edges[i][1] - 1;
    for (size_t i = 0; i < n; ++i) { qsort(children + start[i],(size_t)degree[i],sizeof(*children),compare); cursor[i] = 0; }
    int* counts = calloc(n,sizeof(*counts)); int unmet = 0; size_t total = 0;
    for (size_t i = 0; i < n; ++i) { unmet += target[i] > 0; total += target[i]; }
    int* order = malloc((total + 1) * sizeof(*order)); size_t length = 0; bool valid = true;
    while (unmet) {
        int node = 0;
        while (degree[node]) { int next = children[start[node] + cursor[node]]; cursor[node] = (cursor[node] + 1) % degree[node]; node = next; }
        ++counts[node]; order[length++] = node;
        if (counts[node] > target[node]) { valid = false; break; }
        if (3 * (counts[node] - 1) < target[node] && target[node] <= 3 * counts[node]) --unmet;
    }
    int* answer = malloc((length ? length : 1) * sizeof(*answer));
    if (!valid) answer[0] = -1;
    else {
        int* remaining = malloc(n * sizeof(*remaining)); memcpy(remaining,target,n * sizeof(*remaining));
        for (size_t i = 0; i < length; ++i) { int node = order[i]; --counts[node]; int value = remaining[node] - 3 * counts[node]; if (value < 1) value = 1; answer[i] = value; remaining[node] -= value; }
        free(remaining);
    }
    free(degree); free(start); free(children); free(cursor); free(counts); free(order);
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
// static int compare(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }  // 자식 노드 번호를 작은 값부터 정렬
// int* solution(int** edges, size_t edges_rows, size_t edges_cols, int target[], size_t target_len) {  // 공의 값은 도착 리프에 영향을 주지 않음; 리프마다 공 개수 c에 대해 c≤target≤3c가 처음 모두 성립할 때 멈추기
//     (void)edges_cols; size_t n = target_len; int* degree = calloc(n,sizeof(*degree)); size_t* start = calloc(n + 1,sizeof(*start));  // 노드별 자식 수 / 노드별 자식 목록 시작 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < edges_rows; ++i) ++degree[edges[i][0] - 1];  // 간선 노드 또는 공 위치 순서대로 확인; 노드별 자식 수 갱신
//     for (size_t i = 0; i < n; ++i) start[i + 1] = start[i] + degree[i];  // 간선 노드 또는 공 위치 순서대로 확인; 노드별 자식 목록 시작 갱신
//     int* children = malloc(edges_rows * sizeof(*children)); size_t* cursor = malloc(n * sizeof(*cursor)); memcpy(cursor,start,n * sizeof(*cursor));  // 번호순 자식 목록 / 노드별 다음으로 떨어뜨릴 자식 공간 확보
//     for (size_t i = 0; i < edges_rows; ++i) children[cursor[edges[i][0] - 1]++] = edges[i][1] - 1;  // 간선 노드 또는 공 위치 순서대로 확인; 번호순 자식 목록 / 노드별 다음으로 떨어뜨릴 자식 / 간선 노드 또는 공 위치 확인
//     for (size_t i = 0; i < n; ++i) { qsort(children + start[i],(size_t)degree[i],sizeof(*children),compare); cursor[i] = 0; }  // 간선 노드 또는 공 위치 순서대로 확인; 번호순 자식 목록 / 노드별 자식 목록 시작 정렬 순서 맞추기
//     int* counts = calloc(n,sizeof(*counts)); int unmet = 0; size_t total = 0;  // 리프별 공이 도달한 횟수 / 1부터 3으로 아직 목표를 못 만드는 리프 수 / 목표값 총합 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < n; ++i) { unmet += target[i] > 0; total += target[i]; }  // 간선 노드 또는 공 위치 순서대로 확인; 1부터 3으로 아직 목표를 못 만드는 리프 수 / 간선 노드 또는 공 위치 / 목표값 총합 더해 누적
//     int* order = malloc((total + 1) * sizeof(*order)); size_t length = 0; bool valid = true;  // 공이 떨어진 리프 순서 / 떨어뜨린 공 수 / 목표를 넘기지 않고 끝낼 수 있는지 여부 공간 확보
//     while (unmet) {  // 1부터 3으로 아직 목표를 못 만드는 리프 수가 남아 있으면 반복
//         int node = 0;  // 이번 공이 내려갈 노드 저장
//         while (degree[node]) { int next = children[start[node] + cursor[node]]; cursor[node] = (cursor[node] + 1) % degree[node]; node = next; }  // 리프가 나올 때까지 각 노드의 다음 자식으로 떨어뜨리고 자식 순서 순환
//         ++counts[node]; order[length++] = node;  // 리프별 공이 도달한 횟수 / 떨어뜨린 공 수 갱신
//         if (counts[node] > target[node]) { valid = false; break; }  // 이 리프에 떨어진 공 개수가 목표보다 많으면 더 진행해도 불가능
//         if (3 * (counts[node] - 1) < target[node] && target[node] <= 3 * counts[node]) --unmet;  // 이번 낙하로 목표 합을 만들 최소 횟수를 충족한 리프는 미충족 수에서 제외
//     }  // 이 범위 끝
//     int* answer = malloc((length ? length : 1) * sizeof(*answer));  // 사전순 최소 낙하 값 순서 공간 확보
//     if (!valid) answer[0] = -1;  // 목표를 넘기지 않고 끝낼 수 있는지 여부가 없으면 사전순 최소 낙하 값 순서 갱신
//     else {  // 공 개수가 충분해졌으면 떨어진 순서에 맞춰 가장 작은 숫자부터 배정
//         int* remaining = malloc(n * sizeof(*remaining)); memcpy(remaining,target,n * sizeof(*remaining));  // 리프별 아직 채워야 하는 목표 공간 확보
//         for (size_t i = 0; i < length; ++i) { int node = order[i]; --counts[node]; int value = remaining[node] - 3 * counts[node]; if (value < 1) value = 1; answer[i] = value; remaining[node] -= value; }  // 간선 노드 또는 공 위치 순서대로 확인; 이번 공이 내려갈 노드 / 이번 공에 붙일 최소 1 2 3 값 / 사전순 최소 낙하 값 순서 저장
//         free(remaining);  // 리프별 아직 채워야 하는 목표 임시 공간 정리
//     }  // 이 범위 끝
//     free(degree); free(start); free(children); free(cursor); free(counts); free(order);  // 노드별 자식 수 / 노드별 자식 목록 시작 / 번호순 자식 목록 / 노드별 다음으로 떨어뜨릴 자식 임시 공간 정리
//     return answer;  // 사전순 최소 낙하 값 순서 반환
// }  // 이 범위 끝

// 풀이 요약
// 공의 값은 도착 리프에 영향을 주지 않음; 리프마다 공 개수 c에 대해 c≤target≤3c가 처음 모두 성립할 때 멈추기
// 이후 앞자리부터 가능한 가장 작은 값을 선택; 예: 목표 7에 공 3개면 [1,3,3]으로 배정하기
// 공 수를 B, 트리 높이를 H라 하면 시간 O(B*H+n*log n), 공간 O(B+n)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_150364_1%2C2%2C3_%EB%96%A8%EC%96%B4%ED%8A%B8%EB%A6%AC%EA%B8%B0/README.md)
