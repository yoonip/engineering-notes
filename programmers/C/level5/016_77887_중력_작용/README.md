# 중력 작용 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/77887?language=c)

레벨 5 · C

## 풀이 요약

무거운 자식을 먼저 방문하는 중경로 분해 순서로 정점 위치 고정; 각 중경로와 각 서브트리가 모두 연속 구간

정점이 아닌 값 항목을 암시적 트립으로 관리하고 각 항목에 구간 길이와 64비트 합 저장

서브트리 조회는 고정 구간의 양 끝 접두 합 차이로 계산

루트에서 대상 정점까지의 중경로 조각을 위에서 아래로 처리; 마지막 값 항목을 잘라 전달받은 값으로 바꾸고 구간 맨 앞에 붙이기

구간 길이는 그대로이므로 경로 밖 정점의 위치와 값은 유지되고 구간 사이에는 부모의 예전 값이 순서대로 전달됨

기존 값 항목을 재사용하므로 추가 항목 없이 N개만 유지; 깊은 원래 트리의 전처리는 모두 반복문으로 처리

N개 정점과 Q개 쿼리에서 기대 시간 O(N+Q log²N), 합 조회 한 번은 기대 O(logN), 보조 공간 O(N); 반환 배열은 별도

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct { int left, right, size; uint64_t priority; long long value, sum; } Item;
typedef struct { int n, root; Item* item; int* parent; int* size; int* head; int* position; } Gravity;

static uint64_t priority_for(uint64_t index) {
    uint64_t mixed = index + UINT64_C(0x9e3779b97f4a7c15);
    mixed = (mixed ^ (mixed >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
    mixed = (mixed ^ (mixed >> 27)) * UINT64_C(0x94d049bb133111eb);
    return mixed ^ (mixed >> 31);
}

static void pull(Item* item, int node) {
    item[node].size = item[item[node].left].size + item[item[node].right].size + 1;
    item[node].sum = item[item[node].left].sum + item[node].value + item[item[node].right].sum;
}

static int merge(Item* item, int left, int right) {
    if (!left || !right) return left ? left : right;
    if (item[left].priority > item[right].priority) {
        item[left].right = merge(item, item[left].right, right);
        pull(item, left);
        return left;
    }
    item[right].left = merge(item, left, item[right].left);
    pull(item, right);
    return right;
}

static void split(Item* item, int node, int count, int* left, int* right) {
    if (!node) { *left = 0; *right = 0; return; }
    int before = item[item[node].left].size;
    if (count <= before) {
        split(item, item[node].left, count, left, &item[node].left);
        pull(item, node);
        *right = node;
    } else {
        split(item, item[node].right, count - before - 1, &item[node].right, right);
        pull(item, node);
        *left = node;
    }
}

static long long prefix_sum(const Item* item, int node, int count) {
    long long result = 0;
    while (node && count > 0) {
        int before = item[item[node].left].size;
        if (count <= before) node = item[node].left;
        else {
            result += item[item[node].left].sum + item[node].value;
            count -= before + 1;
            node = item[node].right;
        }
    }
    return result;
}

static void prepare(Gravity* state, const int* values, const int* first, const int* to, const int* next, int* heavy, int* work) {
    int used = 1; work[0] = 0; state->parent[0] = -1;
    for (int index = 0; index < used; ++index) {
        int node = work[index];
        for (int edge = first[node]; edge != -1; edge = next[edge]) {
            int child = to[edge];
            if (child == state->parent[node]) continue;
            state->parent[child] = node; work[used++] = child;
        }
    }
    for (int index = state->n - 1; index >= 0; --index) {
        int node = work[index]; state->size[node] = 1; heavy[node] = -1;
        for (int edge = first[node]; edge != -1; edge = next[edge]) {
            int child = to[edge];
            if (child == state->parent[node]) continue;
            state->size[node] += state->size[child];
            if (heavy[node] == -1 || state->size[child] > state->size[heavy[node]]) heavy[node] = child;
        }
    }
    int pending = 1, timer = 0; work[0] = 0;
    while (pending) {
        int head = work[--pending];
        for (int node = head; node != -1; node = heavy[node]) {
            state->head[node] = head; state->position[node] = timer;
            int entry = ++timer; state->item[entry].value = values[node];
            state->item[entry].priority = priority_for((uint64_t)entry);
            for (int edge = first[node]; edge != -1; edge = next[edge]) {
                int child = to[edge];
                if (child != state->parent[node] && child != heavy[node]) work[pending++] = child;
            }
        }
    }
    int top = 0;
    for (int entry = 1; entry <= state->n; ++entry) {
        int previous = 0;
        while (top && state->item[work[top - 1]].priority < state->item[entry].priority) previous = work[--top];
        state->item[entry].left = previous;
        if (top) state->item[work[top - 1]].right = entry;
        else state->root = entry;
        work[top++] = entry;
    }
    used = 1; work[0] = state->root;
    for (int index = 0; index < used; ++index) {
        int entry = work[index];
        if (state->item[entry].left) work[used++] = state->item[entry].left;
        if (state->item[entry].right) work[used++] = state->item[entry].right;
    }
    for (int index = state->n - 1; index >= 0; --index) pull(state->item, work[index]);
}

static void move_values(Gravity* state, int node, long long incoming) {
    int tails[64], count = 0;
    for (int current = node; current != -1; current = state->parent[state->head[current]]) tails[count++] = current;
    for (int index = count - 1; index >= 0; --index) {
        int tail = tails[index], first = state->position[state->head[tail]];
        int length = state->position[tail] - first + 1;
        int before, rest, path, after, middle, last;
        split(state->item, state->root, first, &before, &rest);
        split(state->item, rest, length, &path, &after);
        split(state->item, path, length - 1, &middle, &last);
        long long outgoing = state->item[last].value;
        state->item[last].value = incoming; state->item[last].sum = incoming;
        path = merge(state->item, last, middle);
        state->root = merge(state->item, merge(state->item, before, path), after);
        incoming = outgoing;
    }
}

static long long subtree_sum(const Gravity* state, int node) {
    int first = state->position[node], end = first + state->size[node];
    return prefix_sum(state->item, state->root, end) - prefix_sum(state->item, state->root, first);
}

long long* solution(int values[], size_t values_len, int** edges, size_t edges_rows, size_t edges_cols, int** queries, size_t queries_rows, size_t queries_cols) {
    (void)edges_cols; (void)queries_cols;
    int n = (int)values_len, edge_count = 0;
    int* first = malloc((size_t)n * sizeof(*first));
    int* to = malloc(2 * edges_rows * sizeof(*to));
    int* next = malloc(2 * edges_rows * sizeof(*next));
    for (int node = 0; node < n; ++node) first[node] = -1;
    for (size_t index = 0; index < edges_rows; ++index) {
        int a = edges[index][0] - 1, b = edges[index][1] - 1;
        to[edge_count] = b; next[edge_count] = first[a]; first[a] = edge_count++;
        to[edge_count] = a; next[edge_count] = first[b]; first[b] = edge_count++;
    }
    Gravity state = {0}; state.n = n;
    state.item = calloc((size_t)n + 1, sizeof(*state.item));
    state.parent = malloc((size_t)n * sizeof(*state.parent));
    state.size = malloc((size_t)n * sizeof(*state.size));
    state.head = malloc((size_t)n * sizeof(*state.head));
    state.position = malloc((size_t)n * sizeof(*state.position));
    int* heavy = malloc((size_t)n * sizeof(*heavy));
    int* work = malloc((size_t)n * sizeof(*work));
    prepare(&state, values, first, to, next, heavy, work);
    free(first); free(to); free(next); free(heavy); free(work);
    size_t answer_count = 0;
    for (size_t index = 0; index < queries_rows; ++index) if (queries[index][1] == -1) ++answer_count;
    long long* answer = malloc((answer_count ? answer_count : 1) * sizeof(*answer));
    size_t written = 0;
    for (size_t index = 0; index < queries_rows; ++index) {
        int node = queries[index][0] - 1, value = queries[index][1];
        if (value == -1) answer[written++] = subtree_sum(&state, node);
        else move_values(&state, node, value);
    }
    free(state.item); free(state.parent); free(state.size); free(state.head); free(state.position);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 입력 배열 길이를 받는 size_t
// #include <stdint.h>  // 트립 우선순위에 쓸 64비트 정수
// #include <stdlib.h>  // 트리·트립 배열과 반환 배열의 동적 할당 및 해제
// 
// typedef struct { int left, right, size; uint64_t priority; long long value, sum; } Item;  // 값 항목의 양쪽 자식, 항목 수, 무작위 우선순위와 구간 합
// typedef struct { int n, root; Item* item; int* parent; int* size; int* head; int* position; } Gravity;  // 값 순서 트립의 루트와 고정된 트리 정점의 부모·서브트리 크기·중경로 정보
// 
// static uint64_t priority_for(uint64_t index) {  // 항목 번호를 섞어 트립의 고정 우선순위 만들기
//     uint64_t mixed = index + UINT64_C(0x9e3779b97f4a7c15);  // 서로 다른 항목 번호에 일정한 비트 패턴 더하기
//     mixed = (mixed ^ (mixed >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);  // 상위 비트와 하위 비트를 첫 번째 곱셈으로 섞기
//     mixed = (mixed ^ (mixed >> 27)) * UINT64_C(0x94d049bb133111eb);  // 두 번째 비트 혼합으로 번호 순서와 우선순위 순서 분리
//     return mixed ^ (mixed >> 31);  // 마지막 비트 혼합 결과를 우선순위로 사용
// }  // 항목 우선순위 생성 끝
// 
// static void pull(Item* item, int node) {  // 자식이 바뀐 항목의 크기와 합 다시 계산
//     item[node].size = item[item[node].left].size + item[item[node].right].size + 1;  // 왼쪽·오른쪽 항목 수에 현재 항목 하나 더하기
//     item[node].sum = item[item[node].left].sum + item[node].value + item[item[node].right].sum;  // 두 자식 구간 합과 현재 값 합치기
// }  // 트립 구간 정보 갱신 끝
// 
// static int merge(Item* item, int left, int right) {  // 왼쪽 순서 뒤에 오른쪽 순서를 이어 붙이기
//     if (!left || !right) return left ? left : right;  // 한쪽이 비었으면 다른 쪽 순서가 그대로 결과
//     if (item[left].priority > item[right].priority) {  // 왼쪽 루트의 우선순위가 높으면 결과 루트로 유지
//         item[left].right = merge(item, item[left].right, right);  // 왼쪽 루트의 뒷부분과 오른쪽 전체를 연결
//         pull(item, left);  // 바뀐 오른쪽 자식에 맞춰 크기와 합 갱신
//         return left;  // 왼쪽 루트를 합친 순서의 루트로 반환
//     }  // 왼쪽 루트를 유지하는 경우 끝
//     item[right].left = merge(item, left, item[right].left);  // 오른쪽 루트 앞부분에 왼쪽 전체를 연결
//     pull(item, right);  // 바뀐 왼쪽 자식에 맞춰 크기와 합 갱신
//     return right;  // 오른쪽 루트를 합친 순서의 루트로 반환
// }  // 두 연속 순서 합치기 끝
// 
// static void split(Item* item, int node, int count, int* left, int* right) {  // 앞 count개 항목과 나머지 항목으로 순서 나누기
//     if (!node) { *left = 0; *right = 0; return; }  // 빈 순서를 나누면 양쪽 모두 빈 트립
//     int before = item[item[node].left].size;  // 현재 항목보다 앞에 있는 왼쪽 구간 길이
//     if (count <= before) {  // 분할 위치가 왼쪽 자식 안이나 현재 항목 바로 앞에 있으면
//         split(item, item[node].left, count, left, &item[node].left);  // 왼쪽 자식을 나누고 뒷부분만 현재 항목 아래에 남기기
//         pull(item, node);  // 줄어든 왼쪽 구간을 크기와 합에 반영
//         *right = node;  // 현재 항목은 분할 결과의 뒷부분 루트
//     } else {  // 현재 항목까지 앞부분에 포함되는 경우
//         split(item, item[node].right, count - before - 1, &item[node].right, right);  // 이미 포함한 왼쪽 구간과 현재 항목을 뺀 나머지 길이로 오른쪽 분할
//         pull(item, node);  // 줄어든 오른쪽 구간을 크기와 합에 반영
//         *left = node;  // 현재 항목은 분할 결과의 앞부분 루트
//     }  // 분할 위치에 따른 자식 처리 끝
// }  // 순서의 길이를 기준으로 한 분할 끝
// 
// static long long prefix_sum(const Item* item, int node, int count) {  // 앞 count개 값의 합을 트립을 바꾸지 않고 구하기
//     long long result = 0;  // 완전히 포함한 앞쪽 구간들의 누적 합
//     while (node && count > 0) {  // 필요한 항목이 남아 있는 동안 분할 위치를 따라 내려가기
//         int before = item[item[node].left].size;  // 현재 항목 앞에 놓인 항목 수
//         if (count <= before) node = item[node].left;  // 필요한 앞부분이 왼쪽 자식 안에만 있으면 그쪽으로 이동
//         else {  // 왼쪽 구간과 현재 값을 모두 포함하는 경우
//             result += item[item[node].left].sum + item[node].value;  // 완전히 포함되는 왼쪽 구간과 현재 값 더하기
//             count -= before + 1;  // 이미 더한 항목 수를 필요한 길이에서 빼기
//             node = item[node].right;  // 아직 필요한 값은 오른쪽 구간에서 찾기
//         }  // 이번 항목을 기준으로 한 앞부분 처리 끝
//     }  // 요청한 앞부분 합산 끝
//     return result;  // 앞 count개였던 원래 요청 구간의 합 반환
// }  // 순서의 접두 구간 합 계산 끝
// 
// static void prepare(Gravity* state, const int* values, const int* first, const int* to, const int* next, int* heavy, int* work) {  // 중경로 분해와 초기 값 순서 트립을 반복문으로 만들기
//     int used = 1; work[0] = 0; state->parent[0] = -1;  // 1번 정점을 루트로 두고 부모가 먼저 오는 정점 순서 시작
//     for (int index = 0; index < used; ++index) {  // 발견한 정점의 자식을 차례로 순서 뒤에 추가
//         int node = work[index];  // 이번에 자식을 찾을 정점
//         for (int edge = first[node]; edge != -1; edge = next[edge]) {  // 현재 정점에 연결된 모든 간선 확인
//             int child = to[edge];  // 간선 반대편 정점
//             if (child == state->parent[node]) continue;  // 이미 온 부모 방향은 자식 탐색에서 제외
//             state->parent[child] = node; work[used++] = child;  // 자식의 부모를 기록하고 나중에 방문할 순서에 추가
//         }  // 현재 정점의 모든 자식 발견 끝
//     }  // 전체 정점의 부모와 부모 우선 순서 확정
//     for (int index = state->n - 1; index >= 0; --index) {  // 자식부터 처리해 서브트리 크기와 무거운 자식 계산
//         int node = work[index]; state->size[node] = 1; heavy[node] = -1;  // 자기 정점 하나로 시작하고 아직 무거운 자식은 없음
//         for (int edge = first[node]; edge != -1; edge = next[edge]) {  // 각 자식 서브트리 크기를 합산
//             int child = to[edge];  // 이번에 합칠 이웃 정점
//             if (child == state->parent[node]) continue;  // 부모는 현재 서브트리의 구성원이 아님
//             state->size[node] += state->size[child];  // 자식 서브트리 전체를 현재 서브트리 크기에 더하기
//             if (heavy[node] == -1 || state->size[child] > state->size[heavy[node]]) heavy[node] = child;  // 가장 큰 자식 서브트리를 중경로의 다음 정점으로 선택
//         }  // 현재 정점의 서브트리 정보 계산 끝
//     }  // 모든 서브트리 크기와 무거운 간선 확정
//     int pending = 1, timer = 0; work[0] = 0;  // 아직 처리하지 않은 중경로 시작점과 다음 고정 배열 위치
//     while (pending) {  // 남은 중경로를 하나씩 무거운 자식 우선으로 펼치기
//         int head = work[--pending];  // 이번 중경로의 가장 위 정점
//         for (int node = head; node != -1; node = heavy[node]) {  // 무거운 자식으로 이어진 정점을 연속 위치에 배치
//             state->head[node] = head; state->position[node] = timer;  // 정점의 중경로 시작점과 고정된 순서 위치 기록
//             int entry = ++timer; state->item[entry].value = values[node];  // 이 위치의 초기 값 항목을 1부터인 트립 번호에 저장
//             state->item[entry].priority = priority_for((uint64_t)entry);  // 값 항목마다 이동 중에도 바뀌지 않을 우선순위 지정
//             for (int edge = first[node]; edge != -1; edge = next[edge]) {  // 중경로 밖 자식은 나중에 별도 경로로 처리
//                 int child = to[edge];  // 다음에 처리할 가벼운 자식 후보
//                 if (child != state->parent[node] && child != heavy[node]) work[pending++] = child;  // 가벼운 자식을 스택에 넣어 깊은 쪽 서브트리부터 마무리
//             }  // 현재 정점의 가벼운 자식 예약 끝
//         }  // 이번 중경로를 연속 위치에 배치 완료
//     }  // 모든 중경로와 서브트리가 각각 연속인 정점 순서 완성
//     int top = 0;  // 초기 순서 트립을 선형 시간에 만들 우선순위 스택 길이
//     for (int entry = 1; entry <= state->n; ++entry) {  // 값의 순서대로 Cartesian 트리 구성
//         int previous = 0;  // 새 항목의 왼쪽 자식이 될 마지막 분리 구간
//         while (top && state->item[work[top - 1]].priority < state->item[entry].priority) previous = work[--top];  // 우선순위가 낮은 스택 끝 항목을 새 항목 아래로 옮기기
//         state->item[entry].left = previous;  // 앞서 분리된 구간을 새 항목의 왼쪽에 연결
//         if (top) state->item[work[top - 1]].right = entry;  // 남은 상위 항목이 있으면 그 오른쪽에 새 항목 연결
//         else state->root = entry;  // 더 높은 항목이 없으면 새 항목이 전체 루트
//         work[top++] = entry;  // 새 항목을 오른쪽 끝 경로의 스택에 추가
//     }  // 초기 순서와 우선순위를 모두 지키는 트립 연결 완료
//     used = 1; work[0] = state->root;  // 트립 합을 아래부터 계산할 부모 우선 순서 시작
//     for (int index = 0; index < used; ++index) {  // 트립의 모든 항목을 재귀 없이 순서에 넣기
//         int entry = work[index];  // 이번에 자식을 찾을 값 항목
//         if (state->item[entry].left) work[used++] = state->item[entry].left;  // 존재하는 왼쪽 자식을 뒤에 추가
//         if (state->item[entry].right) work[used++] = state->item[entry].right;  // 존재하는 오른쪽 자식을 뒤에 추가
//     }  // 트립의 부모 우선 순서 완성
//     for (int index = state->n - 1; index >= 0; --index) pull(state->item, work[index]);  // 자식부터 각 구간 길이와 64비트 합 채우기
// }  // 비재귀 중경로 분해와 초기 트립 구성 끝
// 
// static void move_values(Gravity* state, int node, long long incoming) {  // 루트부터 node까지 값을 한 칸 내리고 루트에 새 값 넣기
//     int tails[64], count = 0;  // 가벼운 간선마다 서브트리 크기가 절반 이하라 100000개 정점의 경로 조각은 64개 미만
//     for (int current = node; current != -1; current = state->parent[state->head[current]]) tails[count++] = current;  // 아래쪽부터 각 중경로 구간의 마지막 정점 수집
//     for (int index = count - 1; index >= 0; --index) {  // 부모의 예전 값을 넘길 수 있도록 루트 쪽 구간부터 처리
//         int tail = tails[index], first = state->position[state->head[tail]];  // 현재 경로 조각의 고정 배열 시작 위치
//         int length = state->position[tail] - first + 1;  // 이 중경로에서 값을 내릴 정점 수
//         int before, rest, path, after, middle, last;  // 앞 구간·경로 조각·뒷 구간과 경로의 마지막 항목을 분리할 루트들
//         split(state->item, state->root, first, &before, &rest);  // 경로 조각 앞의 값 순서는 그대로 떼어두기
//         split(state->item, rest, length, &path, &after);  // 이번 경로 조각과 그 뒤의 값 순서 나누기
//         split(state->item, path, length - 1, &middle, &last);  // 아래쪽 구간으로 넘길 마지막 값 항목 하나를 분리
//         long long outgoing = state->item[last].value;  // 다음 중경로의 맨 앞에 넣을 현재 구간의 예전 마지막 값
//         state->item[last].value = incoming; state->item[last].sum = incoming;  // 재사용할 단일 항목에 위쪽 구간에서 내려온 값 저장
//         path = merge(state->item, last, middle);  // 새 값을 맨 앞에 붙여 구간 안의 기존 값들을 한 칸씩 뒤로 밀기
//         state->root = merge(state->item, merge(state->item, before, path), after);  // 경로 밖의 고정 위치를 유지하며 전체 순서 복원
//         incoming = outgoing;  // 이번 구간 끝의 예전 값을 다음 아래쪽 구간으로 전달
//     }  // 루트에서 선택 정점까지의 모든 값 이동 완료
// }  // 경로 밖 정점의 값을 유지하는 중력 작용 끝
// 
// static long long subtree_sum(const Gravity* state, int node) {  // 고정된 서브트리 구간의 현재 값 합 계산
//     int first = state->position[node], end = first + state->size[node];  // 중경로 우선 DFS에서 서브트리가 차지하는 반열린 구간
//     return prefix_sum(state->item, state->root, end) - prefix_sum(state->item, state->root, first);  // 구간 끝까지의 합에서 시작 전까지의 합 빼기
// }  // 서브트리 합 조회 끝
// 
// long long* solution(int values[], size_t values_len, int** edges, size_t edges_rows, size_t edges_cols, int** queries, size_t queries_rows, size_t queries_cols) {  // 중력 작용을 순서대로 반영하고 서브트리 합만 반환 배열에 저장
//     (void)edges_cols; (void)queries_cols;  // 간선과 쿼리는 각각 두 정수이므로 열 수는 별도로 쓰지 않음
//     int n = (int)values_len, edge_count = 0;  // 고정 트리 정점 수와 양방향 간선 배열의 다음 위치
//     int* first = malloc((size_t)n * sizeof(*first));  // 각 정점에서 시작하는 연결 리스트의 첫 간선 위치
//     int* to = malloc(2 * edges_rows * sizeof(*to));  // 무방향 간선을 양쪽 방향으로 저장할 도착 정점 배열
//     int* next = malloc(2 * edges_rows * sizeof(*next));  // 같은 출발 정점의 다음 간선 위치
//     for (int node = 0; node < n; ++node) first[node] = -1;  // 처음에는 각 정점에 연결된 간선이 없음
//     for (size_t index = 0; index < edges_rows; ++index) {  // 입력의 무방향 간선을 양방향 연결 리스트로 변환
//         int a = edges[index][0] - 1, b = edges[index][1] - 1;  // 1부터인 정점 번호를 0부터인 배열 위치로 변환
//         to[edge_count] = b; next[edge_count] = first[a]; first[a] = edge_count++;  // a에서 b로 가는 간선을 a의 연결 리스트 앞에 추가
//         to[edge_count] = a; next[edge_count] = first[b]; first[b] = edge_count++;  // b에서 a로 가는 반대 방향도 추가
//     }  // 트리 인접 간선 구성 끝
//     Gravity state = {0}; state.n = n;  // 비어 있는 값 순서 트립과 고정 정점 정보 문맥 준비
//     state.item = calloc((size_t)n + 1, sizeof(*state.item));  // 값 항목 n개와 크기·합이 0인 빈 항목 하나 초기화
//     state.parent = malloc((size_t)n * sizeof(*state.parent));  // 각 정점의 부모 번호
//     state.size = malloc((size_t)n * sizeof(*state.size));  // 고정된 원래 트리의 서브트리 정점 수
//     state.head = malloc((size_t)n * sizeof(*state.head));  // 각 정점이 속한 중경로의 가장 위 정점
//     state.position = malloc((size_t)n * sizeof(*state.position));  // 각 정점이 계속 사용할 값 순서의 고정 위치
//     int* heavy = malloc((size_t)n * sizeof(*heavy));  // 전처리 중 가장 큰 자식 서브트리의 정점 번호
//     int* work = malloc((size_t)n * sizeof(*work));  // 부모 우선 순서와 중경로 시작점 스택에 재사용할 작업 배열
//     prepare(&state, values, first, to, next, heavy, work);  // 비재귀 트리 전처리와 초기 순서 트립 만들기
//     free(first); free(to); free(next); free(heavy); free(work);  // 쿼리 처리에 필요 없는 인접 간선과 전처리 배열 해제
//     size_t answer_count = 0;  // 반환 배열에 필요한 합 조회 결과 수
//     for (size_t index = 0; index < queries_rows; ++index) if (queries[index][1] == -1) ++answer_count;  // 값 이동 쿼리를 제외하고 합 조회 개수만 세기
//     long long* answer = malloc((answer_count ? answer_count : 1) * sizeof(*answer));  // 빈 결과도 반환 가능한 동적 배열로 준비
//     size_t written = 0;  // 다음 서브트리 합을 기록할 반환 배열 위치
//     for (size_t index = 0; index < queries_rows; ++index) {  // 모든 쿼리를 입력 순서대로 반영
//         int node = queries[index][0] - 1, value = queries[index][1];  // 대상 정점의 배열 위치와 새 루트 값 또는 조회 표시
//         if (value == -1) answer[written++] = subtree_sum(&state, node);  // 조회 쿼리면 현재 서브트리 합을 결과 뒤에 추가
//         else move_values(&state, node, value);  // 이동 쿼리면 루트에서 대상 정점까지 값을 한 칸씩 내리기
//     }  // 모든 중력 작용과 합 조회 처리 끝
//     free(state.item); free(state.parent); free(state.size); free(state.head); free(state.position);  // 결과와 별개인 값 항목과 고정 트리 정보 해제
//     return answer;  // 합 조회 쿼리의 결과를 발생 순서대로 반환
// }  // 중력 작용 풀이 끝

// 풀이 요약
// 무거운 자식을 먼저 방문하는 중경로 분해 순서로 정점 위치 고정; 각 중경로와 각 서브트리가 모두 연속 구간
// 정점이 아닌 값 항목을 암시적 트립으로 관리하고 각 항목에 구간 길이와 64비트 합 저장
// 서브트리 조회는 고정 구간의 양 끝 접두 합 차이로 계산
// 루트에서 대상 정점까지의 중경로 조각을 위에서 아래로 처리; 마지막 값 항목을 잘라 전달받은 값으로 바꾸고 구간 맨 앞에 붙이기
// 구간 길이는 그대로이므로 경로 밖 정점의 위치와 값은 유지되고 구간 사이에는 부모의 예전 값이 순서대로 전달됨
// 기존 값 항목을 재사용하므로 추가 항목 없이 N개만 유지; 깊은 원래 트리의 전처리는 모두 반복문으로 처리
// N개 정점과 Q개 쿼리에서 기대 시간 O(N+Q log²N), 합 조회 한 번은 기대 O(logN), 보조 공간 O(N); 반환 배열은 별도
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
