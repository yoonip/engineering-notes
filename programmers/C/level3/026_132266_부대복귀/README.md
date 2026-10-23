# 부대복귀

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/132266) · Level 3 · C

## 풀이

길이 양방향이므로 각 출발지→목적지 거리와 목적지→각 출발지 거리가 같음; 목적지에서 BFS 한 번으로 모든 답을 계산
거리를 -1로 시작해 도달하지 못한 지역을 그대로 구분하기; 시간 O(N+E+S), 공간 O(N+E)
예: 두 번째 예제에서 5번부터 거리를 구하면 1번까지 2, 단절된 3번은 -1, 5번 자기 자신은 0

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int* solution(int n, int** roads, size_t roads_rows, size_t roads_cols, int sources[], size_t sources_len, int destination) {
    (void)roads_cols; int* head = malloc(((size_t)n + 1) * sizeof(*head)); int* to = malloc(2 * roads_rows * sizeof(*to)); int* next = malloc(2 * roads_rows * sizeof(*next));
    int* distance = malloc(((size_t)n + 1) * sizeof(*distance)); int* queue = malloc(((size_t)n + 1) * sizeof(*queue));
    for (int i = 0; i <= n; ++i) { head[i] = -1; distance[i] = -1; }
    int edge_count = 0;
    for (size_t i = 0; i < roads_rows; ++i) for (int d = 0; d < 2; ++d) { int a = roads[i][d], b = roads[i][1 - d]; to[edge_count] = b; next[edge_count] = head[a]; head[a] = edge_count++; }
    int first = 0, last = 0; queue[last++] = destination; distance[destination] = 0;
    while (first < last) { int node = queue[first++]; for (int e = head[node]; e >= 0; e = next[e]) if (distance[to[e]] < 0) { distance[to[e]] = distance[node] + 1; queue[last++] = to[e]; } }
    int* answer = malloc(sources_len * sizeof(*answer)); for (size_t i = 0; i < sources_len; ++i) answer[i] = distance[sources[i]];
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
// int* solution(int n, int** roads, size_t roads_rows, size_t roads_cols, int sources[], size_t sources_len, int destination) {  // 길이 양방향이므로 각 출발지→목적지 거리와 목적지→각 출발지 거리가 같음; 목적지에서 BFS 한 번으로 모든 답을 계산
//     (void)roads_cols; int* head = malloc(((size_t)n + 1) * sizeof(*head)); int* to = malloc(2 * roads_rows * sizeof(*to)); int* next = malloc(2 * roads_rows * sizeof(*next));  // 정점별 첫 도로 / 도로의 도착 정점 / 같은 정점의 다음 도로 공간 확보
//     int* distance = malloc(((size_t)n + 1) * sizeof(*distance)); int* queue = malloc(((size_t)n + 1) * sizeof(*queue));  // 목적지에서의 최단 거리 / 역방향 BFS 대기 정점 공간 확보
//     for (int i = 0; i <= n; ++i) { head[i] = -1; distance[i] = -1; }  // 도로 또는 소스 위치 순서대로 확인; 정점별 첫 도로 / 목적지에서의 최단 거리 갱신
//     int edge_count = 0;  // 저장한 양방향 도로 수 저장
//     for (size_t i = 0; i < roads_rows; ++i) for (int d = 0; d < 2; ++d) { int a = roads[i][d], b = roads[i][1 - d]; to[edge_count] = b; next[edge_count] = head[a]; head[a] = edge_count++; }  // 도로 또는 소스 위치 순서대로 확인; 양방향 방향 / 저장한 양방향 도로 수 갱신
//     int first = 0, last = 0; queue[last++] = destination; distance[destination] = 0;  // 큐에서 읽을 위치 / 큐에 넣을 위치 / 역방향 BFS 대기 정점 / 목적지에서의 최단 거리 저장
//     while (first < last) { int node = queue[first++]; for (int e = head[node]; e >= 0; e = next[e]) if (distance[to[e]] < 0) { distance[to[e]] = distance[node] + 1; queue[last++] = to[e]; } }  // 큐에 미처리 정점이 남아 있는 동안 너비 우선 탐색을 계속하기
//     int* answer = malloc(sources_len * sizeof(*answer)); for (size_t i = 0; i < sources_len; ++i) answer[i] = distance[sources[i]];  // 부대별 목적지까지의 거리 / 도로 또는 소스 위치 공간 확보
//     free(head); free(to); free(next); free(distance); free(queue);  // 정점별 첫 도로 / 도로의 도착 정점 / 같은 정점의 다음 도로 / 목적지에서의 최단 거리 임시 공간 정리
//     return answer;  // 부대별 목적지까지의 거리 반환
// }  // 이 범위 끝

// 풀이 요약
// 길이 양방향이므로 각 출발지→목적지 거리와 목적지→각 출발지 거리가 같음; 목적지에서 BFS 한 번으로 모든 답을 계산
// 거리를 -1로 시작해 도달하지 못한 지역을 그대로 구분하기; 시간 O(N+E+S), 공간 O(N+E)
// 예: 두 번째 예제에서 5번부터 거리를 구하면 1번까지 2, 단절된 3번은 -1, 5번 자기 자신은 0
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/026_132266_%EB%B6%80%EB%8C%80%EB%B3%B5%EA%B7%80/README.md)
