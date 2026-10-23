#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static int search(unsigned visited, unsigned sheep_mask, const unsigned* children, int n, int* memo) {
    if (memo[visited] >= 0) return memo[visited];
    int sheep = __builtin_popcount(visited & sheep_mask), wolves = __builtin_popcount(visited) - sheep;
    if (wolves >= sheep) return memo[visited] = 0;
    int best = sheep; unsigned available = 0;
    for (int i = 0; i < n; ++i) if (visited & (1u << i)) available |= children[i];
    available &= ~visited;
    while (available) { unsigned bit = available & (0u - available); available ^= bit; int value = search(visited | bit, sheep_mask, children, n, memo); if (value > best) best = value; }
    return memo[visited] = best;
}
int solution(int info[], size_t info_len, int** edges, size_t edges_rows, size_t edges_cols) {
    (void)edges_cols; unsigned* children = calloc(info_len, sizeof(*children)); unsigned sheep = 0;
    for (size_t i = 0; i < edges_rows; ++i) children[edges[i][0]] |= 1u << edges[i][1];
    for (size_t i = 0; i < info_len; ++i) if (!info[i]) sheep |= 1u << i;
    size_t states = (size_t)1 << info_len; int* memo = malloc(states * sizeof(*memo)); for (size_t i = 0; i < states; ++i) memo[i] = -1;
    int answer = search(1, sheep, children, (int)info_len, memo); free(children); free(memo);
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
// static int search(unsigned visited, unsigned sheep_mask, const unsigned* children, int n, int* memo) {  // 모은 노드의 비트 집합 / 양이 있는 노드 비트 / 노드별 자식 비트 집합 / 방문 집합별 최대 양 수 계산용 함수
//     if (memo[visited] >= 0) return memo[visited];  // 같은 노드 방문 집합을 이미 계산했으면 방문 집합별 최대 양 수 / 모은 노드의 비트 집합로 최종값 계산
//     int sheep = __builtin_popcount(visited & sheep_mask), wolves = __builtin_popcount(visited) - sheep;  // 현재 모은 양 수 / 현재 모은 늑대 수 저장
//     if (wolves >= sheep) return memo[visited] = 0;  // 늑대 수가 양 수 이상이면 방문 집합별 최대 양 수 / 모은 노드의 비트 집합로 최종값 계산
//     int best = sheep; unsigned available = 0;  // 이 상태에서 가능한 최대 양 수 / 다음에 방문할 수 있는 노드 저장
//     for (int i = 0; i < n; ++i) if (visited & (1u << i)) available |= children[i];  // 이미 방문한 노드들의 자식을 다음 방문 후보에 합치기
//     available &= ~visited;  // 다음에 방문할 수 있는 노드 / 모은 노드의 비트 집합 확인
//     while (available) { unsigned bit = available & (0u - available); available ^= bit; int value = search(visited | bit, sheep_mask, children, n, memo); if (value > best) best = value; }  // 방문 가능한 자식을 하나씩 골라 가장 많은 양을 모으는 선택 비교
//     return memo[visited] = best;  // 방문 집합별 최대 양 수 / 모은 노드의 비트 집합 / 이 상태에서 가능한 최대 양 수로 최종값 계산
// }  // 이 범위 끝
// int solution(int info[], size_t info_len, int** edges, size_t edges_rows, size_t edges_cols) {  // 방문했던 노드 사이를 다시 이동해도 양·늑대 수는 변하지 않으므로, 현재 위치 대신 방문 집합만 상태로 사용
//     (void)edges_cols; unsigned* children = calloc(info_len, sizeof(*children)); unsigned sheep = 0;  // 노드별 자식 비트 집합 / 현재 모은 양 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < edges_rows; ++i) children[edges[i][0]] |= 1u << edges[i][1];  // 노드 또는 간선 번호 순서대로 확인; 노드별 자식 비트 집합 / 노드 또는 간선 번호 비트 상태 갱신
//     for (size_t i = 0; i < info_len; ++i) if (!info[i]) sheep |= 1u << i;  // 양이 있는 노드만 양 비트 마스크에 표시
//     size_t states = (size_t)1 << info_len; int* memo = malloc(states * sizeof(*memo)); for (size_t i = 0; i < states; ++i) memo[i] = -1;  // 전체 방문 집합 개수 / 방문 집합별 최대 양 수 / 노드 또는 간선 번호 공간 확보
//     int answer = search(1, sheep, children, (int)info_len, memo); free(children); free(memo);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 늑대보다 많게 모을 최대 양 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 방문했던 노드 사이를 다시 이동해도 양·늑대 수는 변하지 않으므로, 현재 위치 대신 방문 집합만 상태로 사용
// 방문한 부모들의 아직 안 간 자식 중 하나를 고르기; 늑대≥양이 되는 선택은 즉시 버리고, 같은 방문 집합은 캐시하기; 시간 O(N2^N), 공간 O(2^N)
// 예: 양이 두 마리·늑대가 한 마리일 때 늑대를 먼저 더 방문하면 즉시 실패하기; 다른 가지의 양을 먼저 모으면 그 늑대도 나중에 안전하게 방문할 수 있음
