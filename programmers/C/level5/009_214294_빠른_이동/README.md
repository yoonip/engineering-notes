# 빠른 이동 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/214294?language=c)

레벨 5 · C

## 풀이 요약

비트셋 Warshall로 모든 도달 관계를 구하고 서로 왕복 가능한 정점을 SCC 하나로 묶기

SCC 안에서는 도로만으로 모든 스탬프를 모은 뒤 원하는 출구까지 이동 가능하므로 SCC DAG만 고려

서로 도달 가능한 서로 다른 SCC 사이에 이분 간선을 두고 최대 매칭 M 계산

SCC 수 K에서 최대 매칭 M을 빼면 전체 SCC를 덮는 최소 도달 사슬 수; 빠른 이동 한 번마다 새 사슬을 시작하므로 답은 K-M-1

1번에서 모든 지점에 도달 가능하므로 이미 방문한 1번으로 돌아가 다음 사슬 시작점에 갈 수 있음

도로 수 E, 비트셋 묶음 수 W=ceil(N/64), SCC 수 K에 대해 시간 O(E+N²W+K³), 보조 공간 O(NW+N)

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

typedef struct { int count, words, stamp; const uint64_t* reach; const int* representative; int* matched; int* seen; } Matching;

static bool augment(Matching* state, int left) {
    int source = state->representative[left];
    for (int right = 0; right < state->count; ++right) {
        if (left == right || state->seen[right] == state->stamp) continue;
        int target = state->representative[right];
        if (!(state->reach[(size_t)source * state->words + target / 64] & (UINT64_C(1) << (target % 64)))) continue;
        state->seen[right] = state->stamp;
        if (state->matched[right] == -1 || augment(state, state->matched[right])) {
            state->matched[right] = left;
            return true;
        }
    }
    return false;
}

int solution(int n, int** roads, size_t roads_rows, size_t roads_cols) {
    (void)roads_cols;
    int words = (n + 63) / 64;
    uint64_t* reach = calloc((size_t)n * words, sizeof(*reach));
    for (int node = 0; node < n; ++node) reach[(size_t)node * words + node / 64] |= UINT64_C(1) << (node % 64);
    for (size_t id = 0; id < roads_rows; ++id) {
        int from = roads[id][0] - 1, to = roads[id][1] - 1;
        reach[(size_t)from * words + to / 64] |= UINT64_C(1) << (to % 64);
    }
    for (int middle = 0; middle < n; ++middle) {
        const uint64_t* through = reach + (size_t)middle * words;
        for (int from = 0; from < n; ++from) {
            uint64_t* row = reach + (size_t)from * words;
            if (!(row[middle / 64] & (UINT64_C(1) << (middle % 64)))) continue;
            for (int word = 0; word < words; ++word) row[word] |= through[word];
        }
    }
    int* component = malloc((size_t)n * sizeof(*component));
    int* representative = malloc((size_t)n * sizeof(*representative));
    for (int node = 0; node < n; ++node) component[node] = -1;
    int count = 0;
    for (int node = 0; node < n; ++node) {
        if (component[node] != -1) continue;
        representative[count] = node;
        for (int other = 0; other < n; ++other) {
            bool forward = (reach[(size_t)node * words + other / 64] & (UINT64_C(1) << (other % 64))) != 0;
            bool backward = (reach[(size_t)other * words + node / 64] & (UINT64_C(1) << (node % 64))) != 0;
            if (forward && backward) component[other] = count;
        }
        ++count;
    }
    int* matched = malloc((size_t)count * sizeof(*matched));
    int* seen = calloc((size_t)count, sizeof(*seen));
    for (int right = 0; right < count; ++right) matched[right] = -1;
    Matching state = {count, words, 0, reach, representative, matched, seen};
    int matches = 0;
    for (int left = 0; left < count; ++left) {
        state.stamp = left + 1;
        if (augment(&state, left)) ++matches;
    }
    int answer = count - matches - 1;
    free(reach); free(component); free(representative);
    free(matched); free(seen);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 도로 배열 길이와 비트셋 행 위치에 쓸 size_t
// #include <stdint.h>  // 한 번에 64개 도달 여부를 합칠 uint64_t
// #include <stdbool.h>  // 교대 경로를 찾았는지 나타낼 bool
// #include <stdlib.h>  // 도달 비트셋과 SCC·매칭 배열의 할당과 해제
// 
// typedef struct { int count, words, stamp; const uint64_t* reach; const int* representative; int* matched; int* seen; } Matching;  // SCC 도달 비트셋과 대표 정점, 오른쪽 매칭 상대와 이번 탐색 방문 표시
// 
// static bool augment(Matching* state, int left) {  // 왼쪽 SCC에서 시작해 매칭 수를 하나 늘릴 교대 경로 찾기
//     int source = state->representative[left];  // 현재 SCC의 도달 관계를 읽을 원래 대표 정점
//     for (int right = 0; right < state->count; ++right) {  // 이어 붙일 수 있는 모든 다음 SCC를 오른쪽 후보로 확인
//         if (left == right || state->seen[right] == state->stamp) continue;  // 자기 SCC와 이번 교대 경로에서 이미 본 오른쪽 후보는 제외
//         int target = state->representative[right];  // 다음 SCC의 원래 대표 정점
//         if (!(state->reach[(size_t)source * state->words + target / 64] & (UINT64_C(1) << (target % 64)))) continue;  // 도로를 따라 도달할 수 없는 SCC는 같은 진행 경로에 연결할 수 없음
//         state->seen[right] = state->stamp;  // 이번 교대 경로에서 이 오른쪽 SCC를 다시 찾지 않도록 표시
//         if (state->matched[right] == -1 || augment(state, state->matched[right])) {  // 빈 후보이거나 기존 왼쪽 상대를 다른 곳으로 옮길 수 있으면
//             state->matched[right] = left;  // 현재 왼쪽 SCC를 이 오른쪽 SCC의 앞부분으로 연결
//             return true;  // 경로 덮개에서 이어 붙일 연결을 하나 더 확보
//         }  // 현재 오른쪽 후보의 매칭 변경 시도 끝
//     }  // 현재 왼쪽 SCC가 사용할 수 있는 교대 경로 확인 끝
//     return false;  // 이번 왼쪽 SCC에서는 매칭 수를 늘릴 수 없음
// }  // 매칭 증가 경로 탐색 끝
// 
// int solution(int n, int** roads, size_t roads_rows, size_t roads_cols) {  // 모든 스탬프를 모을 최소 빠른 이동 횟수 계산
//     (void)roads_cols;  // 각 도로는 출발·도착 두 번호이므로 열 수는 별도로 쓰지 않음
//     int words = (n + 63) / 64;  // 정점 n개의 도달 여부를 담을 64비트 묶음 수
//     uint64_t* reach = calloc((size_t)n * words, sizeof(*reach));  // 출발 정점별 도달 비트셋을 모두 0으로 초기화
//     for (int node = 0; node < n; ++node) reach[(size_t)node * words + node / 64] |= UINT64_C(1) << (node % 64);  // 각 정점은 자기 자신에 도달 가능
//     for (size_t id = 0; id < roads_rows; ++id) {  // 모든 단방향 도로를 초기 도달 관계에 반영
//         int from = roads[id][0] - 1, to = roads[id][1] - 1;  // 1부터 시작하는 두 정점 번호를 0부터인 배열 위치로 변환
//         reach[(size_t)from * words + to / 64] |= UINT64_C(1) << (to % 64);  // 도로의 도착 정점 비트 표시
//     }  // 자기 자신과 직접 도로의 도달 관계 설정 끝
//     for (int middle = 0; middle < n; ++middle) {  // 중간 정점을 하나씩 허용하는 Warshall 도달 폐쇄
//         const uint64_t* through = reach + (size_t)middle * words;  // 중간 정점에서 갈 수 있는 모든 정점 비트셋
//         for (int from = 0; from < n; ++from) {  // 각 출발점이 현재 중간 정점까지 갈 수 있는지 검사
//             uint64_t* row = reach + (size_t)from * words;  // 이번 출발점의 도달 비트셋
//             if (!(row[middle / 64] & (UINT64_C(1) << (middle % 64)))) continue;  // 중간 정점에 못 가면 그 뒤 도달 관계도 추가할 수 없음
//             for (int word = 0; word < words; ++word) row[word] |= through[word];  // 중간 정점을 거쳐 갈 수 있는 정점을 64개씩 합치기
//         }  // 현재 중간 정점을 통한 모든 출발점 갱신 끝
//     }  // 도로를 여러 번 이용한 전체 도달 관계 확정
//     int* component = malloc((size_t)n * sizeof(*component));  // 원래 정점이 속한 SCC 번호
//     int* representative = malloc((size_t)n * sizeof(*representative));  // SCC마다 도달 관계를 읽을 대표 정점
//     for (int node = 0; node < n; ++node) component[node] = -1;  // 아직 SCC를 배정하지 않은 정점 표시
//     int count = 0;  // 지금까지 찾은 SCC 수
//     for (int node = 0; node < n; ++node) {  // 아직 분류하지 않은 정점에서 새 SCC 시작
//         if (component[node] != -1) continue;  // 이전 대표와 서로 도달해 이미 묶인 정점은 제외
//         representative[count] = node;  // 이번 SCC의 대표 정점 기록
//         for (int other = 0; other < n; ++other) {  // 대표와 왕복할 수 있는 모든 정점을 같은 SCC로 묶기
//             bool forward = (reach[(size_t)node * words + other / 64] & (UINT64_C(1) << (other % 64))) != 0;  // 대표에서 상대 정점으로 갈 수 있는지 확인
//             bool backward = (reach[(size_t)other * words + node / 64] & (UINT64_C(1) << (node % 64))) != 0;  // 상대 정점에서도 대표로 돌아올 수 있는지 확인
//             if (forward && backward) component[other] = count;  // 서로 도달 가능하면 한 번의 도로 진행 안에서 모두 방문 가능
//         }  // 이번 SCC에 속한 정점 분류 끝
//         ++count;  // 찾은 SCC 수 증가
//     }  // 사이클을 하나로 접은 DAG의 정점 분류 끝
//     int* matched = malloc((size_t)count * sizeof(*matched));  // 오른쪽 SCC에 이어진 왼쪽 SCC 번호
//     int* seen = calloc((size_t)count, sizeof(*seen));  // 교대 경로별 오른쪽 SCC 방문 시각을 0으로 초기화
//     for (int right = 0; right < count; ++right) matched[right] = -1;  // 처음에는 이어 붙인 SCC 쌍이 없음
//     Matching state = {count, words, 0, reach, representative, matched, seen};  // 도달 관계와 매칭 탐색 배열을 한 문맥으로 묶기
//     int matches = 0;  // 독립된 진행 경로 두 개를 이어 붙이는 매칭 수
//     for (int left = 0; left < count; ++left) {  // 각 SCC를 경로의 앞부분으로 한 번씩 추가 시도
//         state.stamp = left + 1;  // 방문 배열을 지우는 대신 이번 탐색 번호로 구분
//         if (augment(&state, left)) ++matches;  // 교대 경로를 찾으면 경로 덮개의 개수가 하나 줄어듦
//     }  // SCC 도달 관계의 최대 이분 매칭 완성
//     int answer = count - matches - 1;  // 최소 진행 경로 수에서 첫 경로를 빼면 필요한 빠른 이동 횟수
//     free(reach); free(component); free(representative);  // 도달 폐쇄와 SCC 분류 배열 해제
//     free(matched); free(seen);  // 이분 매칭 탐색 배열 해제
//     return answer;  // 모든 지점 스탬프를 모을 최소 빠른 이동 횟수 반환
// }  // 빠른 이동 계산 끝

// 풀이 요약
// 비트셋 Warshall로 모든 도달 관계를 구하고 서로 왕복 가능한 정점을 SCC 하나로 묶기
// SCC 안에서는 도로만으로 모든 스탬프를 모은 뒤 원하는 출구까지 이동 가능하므로 SCC DAG만 고려
// 서로 도달 가능한 서로 다른 SCC 사이에 이분 간선을 두고 최대 매칭 M 계산
// SCC 수 K에서 최대 매칭 M을 빼면 전체 SCC를 덮는 최소 도달 사슬 수; 빠른 이동 한 번마다 새 사슬을 시작하므로 답은 K-M-1
// 1번에서 모든 지점에 도달 가능하므로 이미 방문한 1번으로 돌아가 다음 사슬 시작점에 갈 수 있음
// 도로 수 E, 비트셋 묶음 수 W=ceil(N/64), SCC 수 K에 대해 시간 O(E+N²W+K³), 보조 공간 O(NW+N)
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
