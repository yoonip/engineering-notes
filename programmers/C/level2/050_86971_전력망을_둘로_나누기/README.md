# 전력망을 둘로 나누기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86971) · Level 2 · C

## 풀이

자식으로 가는 전선을 끊으면 자식 부분 트리 s개와 나머지 n-s개로 나뉨; 모든 간선의 |n-2s|를 비교
예: 일자형 4개 송전탑은 가운데 전선을 끊어 2:2, 차이 0.; 시간·공간 O(N)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int walk(int node, int parent, int n, const bool* graph, int* best) {
    int size = 1;
    for (int next = 1; next <= n; ++next) if (next != parent && graph[node * (n + 1) + next]) {
        int child = walk(next, node, n, graph, best), difference = abs(n - 2 * child);
        if (difference < *best) *best = difference;
        size += child;
    }
    return size;
}
int solution(int n, int** wires, size_t wires_rows, size_t wires_cols) {
    (void)wires_cols;
    bool* graph = calloc((size_t)(n + 1) * (n + 1), sizeof(*graph));
    for (size_t i = 0; i < wires_rows; ++i) graph[wires[i][0] * (n + 1) + wires[i][1]] = graph[wires[i][1] * (n + 1) + wires[i][0]] = true;
    int answer = n; walk(1, 0, n, graph, &answer); free(graph);
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
// static int walk(int node, int parent, int n, const bool* graph, int* best) {  // 자식 서브트리 크기로 전력망 분리 차이 확인
//     int size = 1;  // 현재 서브트리 크기 저장
//     for (int next = 1; next <= n; ++next) if (next != parent && graph[node * (n + 1) + next]) {  // 연결된 다음 송전탑 순서대로 확인; 직전에 온 부모 노드가 아닌 이웃이면
//         int child = walk(next, node, n, graph, best), difference = abs(n - 2 * child);  // 자식 쪽 송전탑 수 / 선을 끊었을 때 두 전력망 차이 저장
//         if (difference < *best) *best = difference;  // 이번에 끊은 두 전력망의 노드 수 차이가 더 작으면 답 갱신
//         size += child;  // 현재 서브트리 크기 / 자식 쪽 송전탑 수 더해 누적
//     }  // 이 범위 끝
//     return size;  // 현재 서브트리 크기 반환
// }  // 이 범위 끝
// int solution(int n, int** wires, size_t wires_rows, size_t wires_cols) {  // 자식으로 가는 전선을 끊으면 자식 부분 트리 s개와 나머지 n-s개로 나뉨; 모든 간선의 |n-2s|를 비교
//     (void)wires_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     bool* graph = calloc((size_t)(n + 1) * (n + 1), sizeof(*graph));  // 송전탑 연결 여부 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < wires_rows; ++i) graph[wires[i][0] * (n + 1) + wires[i][1]] = graph[wires[i][1] * (n + 1) + wires[i][0]] = true;  // 송전선 위치 순서대로 확인; 송전탑 연결 여부 / 송전선 위치 확인
//     int answer = n; walk(1, 0, n, graph, &answer); free(graph);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 가능한 최소 송전탑 수 차이 반환
// }  // 이 범위 끝

// 풀이 요약
// 자식으로 가는 전선을 끊으면 자식 부분 트리 s개와 나머지 n-s개로 나뉨; 모든 간선의 |n-2s|를 비교
// 예: 일자형 4개 송전탑은 가운데 전선을 끊어 2:2, 차이 0.; 시간·공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/050_86971_%EC%A0%84%EB%A0%A5%EB%A7%9D%EC%9D%84_%EB%91%98%EB%A1%9C_%EB%82%98%EB%88%84%EA%B8%B0/README.md)
