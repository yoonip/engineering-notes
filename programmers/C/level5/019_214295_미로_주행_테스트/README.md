# 미로 주행 테스트 — C

[레벨 5 목록](../README.md) · [언어별 목록](../../README.md) · [문제](https://school.programmers.co.kr/learn/courses/30/lessons/214295?language=c)

레벨 5 · C

## 풀이 요약

U=X+Y, V=X−Y로 바꾸면 맨해튼 거리 D 이하 조건이 U,V 각각 중심에서 D 이내인 사각형

성공 기록의 사각형은 교집합으로 모으고 실패 기록의 사각형 합집합은 U 스윕과 V 구간 덮임으로 제외

원래 도로 경계는 |V|≤U≤min(2N−V,2M+V), 정수 좌표 조건은 U와 V의 홀짝이 같다는 조건

실패 덮임이 일정한 U 슬랩마다 상·하한 식이 바뀌는 V 경계로 나누고 U 상한이 하한 이상인 범위만 남기기

V=2t+p에서 허용 U 개수는 t의 일차식이므로 미덮임 V의 홀짝별 개수와 t 합만 조회해 격자점 수 합산

압축 리프의 일부만 조회되면 그 정수 구간의 개수와 합을 직접 계산; 음수 좌표의 나눗셈은 수학적 올림·내림으로 처리

테스트 수 Q에 대해 시간 O(Q log Q), 보조 공간 O(Q); 좌표 연산과 가능한 위치 수는 64비트 정수 사용

## 코드와 줄별 설명

[제출 코드](solution.c) · [사이트 채점 기록](grading.json) · [별도 로컬 검사](local_checks.json)

~~~c
#include <stddef.h>
#include <stdlib.h>

typedef struct { long long count[2], moment[2]; } Moments;
typedef struct { Moments available; int cover; } CoverNode;
typedef struct { long long u; int first, last, change; } Event;
typedef struct { CoverNode* node; const int* coordinate; int leaves, base; } CoverTree;

static long long min_ll(long long a, long long b) { return a < b ? a : b; }
static long long max_ll(long long a, long long b) { return a > b ? a : b; }

static long long floor_div(long long value, long long divisor) {
    long long quotient = value / divisor, remainder = value % divisor;
    return quotient - (remainder < 0);
}

static long long ceil_div(long long value, long long divisor) {
    return -floor_div(-value, divisor);
}

static Moments interval_moments(long long low, long long high) {
    Moments result = {{0, 0}, {0, 0}};
    if (low > high) return result;
    for (int parity = 0; parity < 2; ++parity) {
        long long first = ceil_div(low - parity, 2), last = floor_div(high - parity, 2);
        if (first > last) continue;
        result.count[parity] = last - first + 1;
        result.moment[parity] = (first + last) * result.count[parity] / 2;
    }
    return result;
}

static Moments add_moments(Moments a, Moments b) {
    for (int parity = 0; parity < 2; ++parity) {
        a.count[parity] += b.count[parity]; a.moment[parity] += b.moment[parity];
    }
    return a;
}

static void refresh(CoverTree* tree, int node) {
    if (tree->node[node].cover > 0) {
        Moments empty = {{0, 0}, {0, 0}}; tree->node[node].available = empty;
    } else if (node >= tree->base) {
        int leaf = node - tree->base;
        tree->node[node].available = leaf < tree->leaves ? interval_moments(tree->coordinate[leaf], (long long)tree->coordinate[leaf + 1] - 1) : interval_moments(1, 0);
    } else {
        tree->node[node].available = add_moments(tree->node[node * 2].available, tree->node[node * 2 + 1].available);
    }
}

static void change_cover(CoverTree* tree, int node, int left, int right, int first, int last, int change) {
    if (first <= left && right <= last) {
        tree->node[node].cover += change; refresh(tree, node);
        return;
    }
    int middle = (left + right) / 2;
    if (first < middle) change_cover(tree, node * 2, left, middle, first, last, change);
    if (last > middle) change_cover(tree, node * 2 + 1, middle, right, first, last, change);
    refresh(tree, node);
}

static Moments query_moments(const CoverTree* tree, int node, int left, int right, long long low, long long high) {
    Moments empty = {{0, 0}, {0, 0}};
    if (tree->node[node].cover > 0 || left >= tree->leaves) return empty;
    long long start = tree->coordinate[left], end = (long long)tree->coordinate[right < tree->leaves ? right : tree->leaves] - 1;
    if (high < start || end < low) return empty;
    if (low <= start && end <= high) return tree->node[node].available;
    if (right - left == 1) return interval_moments(max_ll(low, start), min_ll(high, end));
    int middle = (left + right) / 2;
    Moments a = query_moments(tree, node * 2, left, middle, low, high);
    Moments b = query_moments(tree, node * 2 + 1, middle, right, low, high);
    return add_moments(a, b);
}

static long long count_slab(const CoverTree* tree, long long left_u, long long right_u, int n, int m) {
    if (left_u > right_u || tree->node[1].available.count[0] + tree->node[1].available.count[1] == 0) return 0;
    long long boundary[6] = {tree->coordinate[0], tree->coordinate[tree->leaves], -left_u, left_u + 1, right_u - 2LL * m, 2LL * n - right_u + 1};
    for (int index = 1; index < 6; ++index) {
        long long value = boundary[index]; int place = index;
        while (place && boundary[place - 1] > value) { boundary[place] = boundary[place - 1]; --place; }
        boundary[place] = value;
    }
    long long answer = 0;
    for (int index = 0; index < 5; ++index) {
        long long low = max_ll(boundary[index], tree->coordinate[0]), high = min_ll(boundary[index + 1] - 1, (long long)tree->coordinate[tree->leaves] - 1);
        if (low > high) continue;
        int lower_a = low < -left_u ? -1 : low > left_u ? 1 : 0;
        long long lower_b = lower_a ? 0 : left_u;
        int upper_a = low < right_u - 2LL * m ? 1 : low > 2LL * n - right_u ? -1 : 0;
        long long upper_b = upper_a == 1 ? 2LL * m : upper_a == -1 ? 2LL * n : right_u;
        int slope = upper_a - lower_a; long long difference = upper_b - lower_b;
        if (slope > 0) low = max_ll(low, ceil_div(-difference, slope));
        else if (slope < 0) high = min_ll(high, floor_div(difference, -slope));
        else if (difference < 0) continue;
        if (low > high) continue;
        Moments available = query_moments(tree, 1, 0, tree->base, low, high);
        for (int parity = 0; parity < 2; ++parity) {
            long long constant = floor_div((upper_a - 1LL) * parity + upper_b, 2) - ceil_div((lower_a - 1LL) * parity + lower_b, 2) + 1;
            answer += slope * available.moment[parity] + constant * available.count[parity];
        }
    }
    return answer;
}

static int compare_int(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b; return (x > y) - (x < y);
}

static int compare_event(const void* a, const void* b) {
    long long x = ((const Event*)a)->u, y = ((const Event*)b)->u; return (x > y) - (x < y);
}

static int coordinate_index(const int* coordinate, int length, int value) {
    int low = 0, high = length;
    while (low < high) {
        int middle = (low + high) / 2;
        if (coordinate[middle] < value) low = middle + 1; else high = middle;
    }
    return low;
}

static long long solve_tests(int n, int m, int* const* tests, size_t rows) {
    long long low_u = 0, high_u = (long long)n + m, low_v = -(long long)m, high_v = n;
    for (size_t index = 0; index < rows; ++index) {
        if (!tests[index][3]) continue;
        long long u = (long long)tests[index][0] + tests[index][1], v = (long long)tests[index][0] - tests[index][1], distance = tests[index][2];
        low_u = max_ll(low_u, u - distance); high_u = min_ll(high_u, u + distance);
        low_v = max_ll(low_v, v - distance); high_v = min_ll(high_v, v + distance);
    }
    if (low_u > high_u || low_v > high_v) return 0;
    Event* event = (Event*)malloc(2 * rows * sizeof(*event));
    int* coordinate = (int*)malloc((2 * rows + 2) * sizeof(*coordinate));
    int event_count = 0, coordinate_count = 2; coordinate[0] = (int)low_v; coordinate[1] = (int)(high_v + 1);
    for (size_t index = 0; index < rows; ++index) {
        if (tests[index][3]) continue;
        long long u = (long long)tests[index][0] + tests[index][1], v = (long long)tests[index][0] - tests[index][1], distance = tests[index][2];
        long long first_u = max_ll(low_u, u - distance), last_u = min_ll(high_u, u + distance);
        long long first_v = max_ll(low_v, v - distance), last_v = min_ll(high_v, v + distance);
        if (first_u > last_u || first_v > last_v) continue;
        event[event_count].u = first_u; event[event_count].first = (int)first_v; event[event_count].last = (int)(last_v + 1); event[event_count++].change = 1;
        event[event_count] = event[event_count - 1]; event[event_count].u = last_u + 1; event[event_count++].change = -1;
        coordinate[coordinate_count++] = (int)first_v; coordinate[coordinate_count++] = (int)(last_v + 1);
    }
    qsort(coordinate, (size_t)coordinate_count, sizeof(*coordinate), compare_int);
    int unique = 0;
    for (int index = 0; index < coordinate_count; ++index) if (!unique || coordinate[index] != coordinate[unique - 1]) coordinate[unique++] = coordinate[index];
    qsort(event, (size_t)event_count, sizeof(*event), compare_event);
    for (int index = 0; index < event_count; ++index) {
        event[index].first = coordinate_index(coordinate, unique, event[index].first);
        event[index].last = coordinate_index(coordinate, unique, event[index].last);
    }
    int base = 1; while (base < unique - 1) base *= 2;
    CoverNode* nodes = (CoverNode*)calloc((size_t)base * 2, sizeof(*nodes));
    CoverTree tree = {nodes, coordinate, unique - 1, base};
    for (int node = base * 2 - 1; node > 0; --node) refresh(&tree, node);
    long long answer = 0, current_u = low_u; int index = 0;
    while (index < event_count) {
        long long next_u = event[index].u;
        answer += count_slab(&tree, current_u, next_u - 1, n, m);
        while (index < event_count && event[index].u == next_u) {
            change_cover(&tree, 1, 0, base, event[index].first, event[index].last, event[index].change);
            ++index;
        }
        current_u = next_u;
    }
    answer += count_slab(&tree, current_u, high_u, n, m);
    free(nodes); free(coordinate); free(event);
    return answer;
}

long long solution(int n, int m, int** tests, size_t tests_rows, size_t tests_cols) {
    (void)tests_cols;
    return solve_tests(n, m, tests, tests_rows);
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 테스트 행 개수를 받는 size_t
// #include <stdlib.h>  // 덮임 트리 배열의 동적 할당과 경계 정렬
// 
// typedef struct { long long count[2], moment[2]; } Moments;  // 덮이지 않은 V를 홀짝별로 세고 V=2t+p의 t 합도 저장
// typedef struct { Moments available; int cover; } CoverNode;  // V 구간의 미덮임 통계와 이 노드 전체를 덮는 실패 사각형 수
// typedef struct { long long u; int first, last, change; } Event;  // U 경계에서 더하거나 뺄 V 반열린 구간; 압축 뒤에는 first·last가 구간 번호
// typedef struct { CoverNode* node; const int* coordinate; int leaves, base; } CoverTree;  // V 좌표 경계와 완전 이진 덮임 트리의 실제 리프 수·밑변 크기
// 
// static long long min_ll(long long a, long long b) { return a < b ? a : b; }  // 좌표 산술을 64비트로 유지하는 최솟값
// static long long max_ll(long long a, long long b) { return a > b ? a : b; }  // 좌표 산술을 64비트로 유지하는 최댓값
// 
// static long long floor_div(long long value, long long divisor) {  // 양수로 나눈 몫을 음수에서도 아래쪽 정수로 내림
//     long long quotient = value / divisor, remainder = value % divisor;  // C의 0 방향 나눗셈 몫과 나머지 확인
//     return quotient - (remainder < 0);  // 음수 나머지가 있으면 실제 내림 몫은 하나 더 작음
// }  // 음수 좌표를 포함한 내림 나눗셈 끝
// 
// static long long ceil_div(long long value, long long divisor) {  // 양수로 나눈 몫을 위쪽 정수로 올림
//     return -floor_div(-value, divisor);  // 부호를 뒤집어 내린 뒤 다시 뒤집으면 올림 몫
// }  // 음수 좌표를 포함한 올림 나눗셈 끝
// 
// static Moments interval_moments(long long low, long long high) {  // 정수 V 구간의 홀짝별 개수와 t 합을 등차수열로 계산
//     Moments result = {{0, 0}, {0, 0}};  // 두 홀짝의 개수와 합을 0으로 시작
//     if (low > high) return result;  // 빈 정수 구간에는 가능한 V가 없음
//     for (int parity = 0; parity < 2; ++parity) {  // V=2t와 V=2t+1을 따로 계산
//         long long first = ceil_div(low - parity, 2), last = floor_div(high - parity, 2);  // 이 구간에 들어오는 t의 양 끝 정수
//         if (first > last) continue;  // 해당 홀짝의 V가 없으면 다음 홀짝으로 이동
//         result.count[parity] = last - first + 1;  // 연속된 t의 개수는 마지막−처음+1
//         result.moment[parity] = (first + last) * result.count[parity] / 2;  // 등차수열 합으로 모든 t의 합 계산
//     }  // 두 홀짝의 정수 구간 통계 완성
//     return result;  // 덮임이 없는 정수 V 구간의 통계 반환
// }  // 홀짝별 구간 모멘트 계산 끝
// 
// static Moments add_moments(Moments a, Moments b) {  // 서로 겹치지 않는 두 V 구간의 통계 합치기
//     for (int parity = 0; parity < 2; ++parity) {  // 두 홀짝을 각각 독립적으로 합산
//         a.count[parity] += b.count[parity]; a.moment[parity] += b.moment[parity];  // 정수 개수와 t 합을 같은 홀짝끼리 더하기
//     }  // 두 홀짝 통계 합산 끝
//     return a;  // 합쳐진 구간 통계 반환
// }  // 구간 모멘트 합치기 끝
// 
// static void refresh(CoverTree* tree, int node) {  // 덮임 수와 자식 통계에 맞춰 미덮임 V 통계 갱신
//     if (tree->node[node].cover > 0) {  // 실패 사각형 하나라도 이 구간 전체를 덮고 있으면
//         Moments empty = {{0, 0}, {0, 0}}; tree->node[node].available = empty;  // 이 구간의 모든 V를 후보에서 제외
//     } else if (node >= tree->base) {  // 덮이지 않은 리프라면 원래 정수 구간을 복구
//         int leaf = node - tree->base;  // 완전 이진 트리의 리프 번호를 압축 구간 번호로 변환
//         tree->node[node].available = leaf < tree->leaves ? interval_moments(tree->coordinate[leaf], (long long)tree->coordinate[leaf + 1] - 1) : interval_moments(1, 0);  // 실제 구간은 등차수열 통계, 밑변을 채운 빈 리프는 0
//     } else {  // 덮이지 않은 내부 구간은 자식의 미덮임 부분만 포함
//         tree->node[node].available = add_moments(tree->node[node * 2].available, tree->node[node * 2 + 1].available);  // 양쪽 자식의 미덮임 통계 합치기
//     }  // 현재 구간의 덮임 여부에 따른 통계 갱신 끝
// }  // 덮임 트리 노드 갱신 끝
// 
// static void change_cover(CoverTree* tree, int node, int left, int right, int first, int last, int change) {  // 압축 V 구간 [first,last)의 실패 덮임 수 증감
//     if (first <= left && right <= last) {  // 현재 트리 구간이 변경 범위에 완전히 포함되면
//         tree->node[node].cover += change; refresh(tree, node);  // 전체 덮임 수를 바꾸고 미덮임 통계 다시 계산
//         return;  // 전체 덮임은 이 노드에 저장하므로 자식까지 내리지 않음
//     }  // 구간 전체를 바꾸는 경우 끝
//     int middle = (left + right) / 2;  // 압축 V 구간을 나눌 가운데 리프 위치
//     if (first < middle) change_cover(tree, node * 2, left, middle, first, last, change);  // 변경 범위와 겹치는 왼쪽 자식 갱신
//     if (last > middle) change_cover(tree, node * 2 + 1, middle, right, first, last, change);  // 변경 범위와 겹치는 오른쪽 자식 갱신
//     refresh(tree, node);  // 바뀐 자식들의 미덮임 통계를 현재 구간에 반영
// }  // 실패 사각형의 V 덮임 변경 끝
// 
// static Moments query_moments(const CoverTree* tree, int node, int left, int right, long long low, long long high) {  // 실제 V 좌표 구간에서 실패 사각형 밖의 홀짝 통계 조회
//     Moments empty = {{0, 0}, {0, 0}};  // 겹침이 없거나 덮인 부분을 나타낼 빈 통계
//     if (tree->node[node].cover > 0 || left >= tree->leaves) return empty;  // 완전히 덮인 구간과 밑변의 빈 리프는 후보가 없음
//     long long start = tree->coordinate[left], end = (long long)tree->coordinate[right < tree->leaves ? right : tree->leaves] - 1;  // 이 노드가 담는 실제 정수 V 구간의 양 끝
//     if (high < start || end < low) return empty;  // 요청 구간과 겹치지 않으면 합산하지 않음
//     if (low <= start && end <= high) return tree->node[node].available;  // 전체가 포함되면 저장해 둔 미덮임 통계 사용
//     if (right - left == 1) return interval_moments(max_ll(low, start), min_ll(high, end));  // 리프 안쪽 경계는 겹친 정수 구간의 등차수열을 직접 계산
//     int middle = (left + right) / 2;  // 부분 조회를 나눌 가운데 압축 위치
//     Moments a = query_moments(tree, node * 2, left, middle, low, high);  // 왼쪽 자식에서 요청 범위의 미덮임 통계 구하기
//     Moments b = query_moments(tree, node * 2 + 1, middle, right, low, high);  // 오른쪽 자식에서 요청 범위의 미덮임 통계 구하기
//     return add_moments(a, b);  // 양쪽의 겹치지 않는 후보 통계 합치기
// }  // 실제 좌표의 미덮임 모멘트 조회 끝
// 
// static long long count_slab(const CoverTree* tree, long long left_u, long long right_u, int n, int m) {  // 실패 덮임 상태가 같은 정수 U 슬랩의 원래 격자점 수 계산
//     if (left_u > right_u || tree->node[1].available.count[0] + tree->node[1].available.count[1] == 0) return 0;  // 빈 슬랩이나 남은 V가 없는 상태는 기여가 없음
//     long long boundary[6] = {tree->coordinate[0], tree->coordinate[tree->leaves], -left_u, left_u + 1, right_u - 2LL * m, 2LL * n - right_u + 1};  // U 하한 max(L,−V,V)와 상한 min(R,2n−V,2m+V)의 식이 바뀌는 V 경계
//     for (int index = 1; index < 6; ++index) {  // 최대 여섯 경계를 작은 삽입 정렬로 정렬
//         long long value = boundary[index]; int place = index;  // 이번 경계값과 끼워 넣을 위치
//         while (place && boundary[place - 1] > value) { boundary[place] = boundary[place - 1]; --place; }  // 더 큰 앞쪽 경계들을 오른쪽으로 밀기
//         boundary[place] = value;  // 현재 경계를 정렬된 위치에 넣기
//     }  // 경계가 바뀌지 않는 V 조각의 순서 확정
//     long long answer = 0;  // 이 U 슬랩에 속하는 가능한 원래 격자점 수
//     for (int index = 0; index < 5; ++index) {  // 각 조각에서는 U 상·하한이 V의 일차식
//         long long low = max_ll(boundary[index], tree->coordinate[0]), high = min_ll(boundary[index + 1] - 1, (long long)tree->coordinate[tree->leaves] - 1);  // 실제 후보 V 범위와 현재 조각의 교집합
//         if (low > high) continue;  // 중복 경계나 후보 범위 밖의 조각은 제외
//         int lower_a = low < -left_u ? -1 : low > left_u ? 1 : 0;  // U 하한이 −V, V, L 중 어느 일차식인지 선택
//         long long lower_b = lower_a ? 0 : left_u;  // 선택한 U 하한의 상수항
//         int upper_a = low < right_u - 2LL * m ? 1 : low > 2LL * n - right_u ? -1 : 0;  // U 상한이 2m+V, 2n−V, R 중 어느 일차식인지 선택
//         long long upper_b = upper_a == 1 ? 2LL * m : upper_a == -1 ? 2LL * n : right_u;  // 선택한 U 상한의 상수항
//         int slope = upper_a - lower_a; long long difference = upper_b - lower_b;  // U 상한−하한의 기울기와 상수항
//         if (slope > 0) low = max_ll(low, ceil_div(-difference, slope));  // U 상한이 하한 이상인 V의 최소 정수로 자르기
//         else if (slope < 0) high = min_ll(high, floor_div(difference, -slope));  // U 상한이 하한 이상인 V의 최대 정수로 자르기
//         else if (difference < 0) continue;  // 평행한 상한이 하한보다 작으면 가능한 U가 없음
//         if (low > high) continue;  // 원래 직사각형과 만나는 V가 없으면 제외
//         Moments available = query_moments(tree, 1, 0, tree->base, low, high);  // 실패 사각형에 덮이지 않은 V의 홀짝별 개수와 t 합 조회
//         for (int parity = 0; parity < 2; ++parity) {  // 정수 X,Y를 복원하려면 U와 V의 홀짝이 같아야 함
//             long long constant = floor_div((upper_a - 1LL) * parity + upper_b, 2) - ceil_div((lower_a - 1LL) * parity + lower_b, 2) + 1;  // V=2t+p일 때 허용되는 U 수의 상수항
//             answer += slope * available.moment[parity] + constant * available.count[parity];  // 각 V의 허용 U 수가 slope*t+constant이므로 모멘트로 한꺼번에 합산
//         }  // 두 홀짝의 원래 정수 격자점 합산 끝
//     }  // U 상·하한 식이 일정한 모든 V 조각 처리 끝
//     return answer;  // 이번 U 슬랩의 후보 표지판 위치 수 반환
// }  // 도로 직사각형과 홀짝 조건을 반영한 슬랩 계수 끝
// 
// static int compare_int(const void* a, const void* b) {  // 좌표 압축용 정수 경계 비교
//     int x = *(const int*)a, y = *(const int*)b; return (x > y) - (x < y);  // 좌표 차를 직접 빼지 않아 비교 중 정수 오버플로 방지
// }  // V 좌표 비교 끝
// 
// static int compare_event(const void* a, const void* b) {  // U가 작은 순서로 실패 사각형 경계 정렬
//     long long x = ((const Event*)a)->u, y = ((const Event*)b)->u; return (x > y) - (x < y);  // 같은 U의 이벤트는 한꺼번에 처리하므로 U만 비교
// }  // U 스윕 이벤트 비교 끝
// 
// static int coordinate_index(const int* coordinate, int length, int value) {  // 압축 배열에서 경계값의 위치를 이분 탐색
//     int low = 0, high = length;  // 경계값이 들어갈 반열린 탐색 범위
//     while (low < high) {  // 후보 위치가 하나로 좁혀질 때까지 반복
//         int middle = (low + high) / 2;  // 이번에 비교할 압축 경계 위치
//         if (coordinate[middle] < value) low = middle + 1; else high = middle;  // 경계값 이상인 첫 위치가 남도록 범위 절반 제거
//     }  // 압축 경계 위치 확정
//     return low;  // 이벤트의 실제 좌표를 압축 구간 번호로 변환한 결과
// }  // 좌표 경계 이분 탐색 끝
// 
// static long long solve_tests(int n, int m, int* const* tests, size_t rows) {  // 성공 기록 교집합에서 실패 기록 사각형 합집합을 제외한 격자점 수 계산
//     long long low_u = 0, high_u = (long long)n + m, low_v = -(long long)m, high_v = n;  // 원래 도로 안의 모든 점이 들어가는 U=X+Y, V=X−Y 바깥 상자
//     for (size_t index = 0; index < rows; ++index) {  // 모든 성공 기록의 맨해튼 공을 U,V 사각형으로 바꾸어 교집합
//         if (!tests[index][3]) continue;  // 실패 기록의 제외 영역은 스윕에서 따로 반영
//         long long u = (long long)tests[index][0] + tests[index][1], v = (long long)tests[index][0] - tests[index][1], distance = tests[index][2];  // 기록 출발점을 변환하고 거리도 64비트로 승격
//         low_u = max_ll(low_u, u - distance); high_u = min_ll(high_u, u + distance);  // 성공 기록이 허용하는 U 범위와 교집합
//         low_v = max_ll(low_v, v - distance); high_v = min_ll(high_v, v + distance);  // 성공 기록이 허용하는 V 범위와 교집합
//     }  // 모든 성공 기록의 후보 상자 확정
//     if (low_u > high_u || low_v > high_v) return 0;  // 성공 조건부터 양립할 수 없으면 후보가 없음
//     Event* event = (Event*)malloc(2 * rows * sizeof(*event));  // 실패 사각형마다 U 시작의 추가와 끝 다음의 제거 이벤트 저장
//     int* coordinate = (int*)malloc((2 * rows + 2) * sizeof(*coordinate));  // 실패 V 구간과 전체 후보 V 구간의 정수 경계 저장
//     int event_count = 0, coordinate_count = 2; coordinate[0] = (int)low_v; coordinate[1] = (int)(high_v + 1);  // V는 [−m,n] 안이므로 끝 다음까지 int에 들어가는 전체 경계부터 준비
//     for (size_t index = 0; index < rows; ++index) {  // 실패 기록에서 후보 상자와 겹치는 제외 사각형만 추출
//         if (tests[index][3]) continue;  // 성공 기록은 이미 교집합으로 반영했으므로 제외
//         long long u = (long long)tests[index][0] + tests[index][1], v = (long long)tests[index][0] - tests[index][1], distance = tests[index][2];  // 실패 기록의 맨해튼 공을 변환할 중심과 거리
//         long long first_u = max_ll(low_u, u - distance), last_u = min_ll(high_u, u + distance);  // 실패 사각형의 U 범위를 후보 상자 안으로 자르기
//         long long first_v = max_ll(low_v, v - distance), last_v = min_ll(high_v, v + distance);  // 실패 사각형의 V 범위를 후보 상자 안으로 자르기
//         if (first_u > last_u || first_v > last_v) continue;  // 성공 후보와 겹치지 않는 실패 기록은 영향이 없음
//         event[event_count].u = first_u; event[event_count].first = (int)first_v; event[event_count].last = (int)(last_v + 1); event[event_count++].change = 1;  // 실패 U 시작점부터 정수 V 구간을 덮기
//         event[event_count] = event[event_count - 1]; event[event_count].u = last_u + 1; event[event_count++].change = -1;  // 실패 U 끝 다음 정수에서 같은 V 구간의 덮임 제거
//         coordinate[coordinate_count++] = (int)first_v; coordinate[coordinate_count++] = (int)(last_v + 1);  // V 구간이 시작하거나 끝나는 경계를 좌표 압축에 추가
//     }  // 모든 유효한 실패 사각형 이벤트 추출 끝
//     qsort(coordinate, (size_t)coordinate_count, sizeof(*coordinate), compare_int);  // V 경계를 오름차순으로 정렬
//     int unique = 0;  // 중복을 지운 V 경계 개수
//     for (int index = 0; index < coordinate_count; ++index) if (!unique || coordinate[index] != coordinate[unique - 1]) coordinate[unique++] = coordinate[index];  // 서로 다른 경계만 앞에서부터 모으기
//     qsort(event, (size_t)event_count, sizeof(*event), compare_event);  // U가 작은 경계부터 실패 덮임을 바꾸도록 정렬
//     for (int index = 0; index < event_count; ++index) {  // 이벤트에 저장한 실제 V 경계를 압축 위치로 변환
//         event[index].first = coordinate_index(coordinate, unique, event[index].first);  // 실패 V 구간의 첫 리프 위치
//         event[index].last = coordinate_index(coordinate, unique, event[index].last);  // 실패 V 구간의 끝 다음 리프 위치
//     }  // 모든 이벤트의 V 좌표 압축 끝
//     int base = 1; while (base < unique - 1) base *= 2;  // 실제 압축 구간 수 이상인 최소 2의 거듭제곱 리프 수
//     CoverNode* nodes = (CoverNode*)calloc((size_t)base * 2, sizeof(*nodes));  // 실패 덮임이 0인 완전 이진 트리 준비
//     CoverTree tree = {nodes, coordinate, unique - 1, base};  // 덮임 통계와 V 경계를 한 조회 문맥으로 묶기
//     for (int node = base * 2 - 1; node > 0; --node) refresh(&tree, node);  // 리프의 정수 통계부터 내부 합까지 아래에서 위로 초기화
//     long long answer = 0, current_u = low_u; int index = 0;  // 누적 후보 수와 아직 세지 않은 첫 U, 다음 이벤트 위치
//     while (index < event_count) {  // 실패 덮임이 바뀌는 U 경계 순서대로 스윕
//         long long next_u = event[index].u;  // 현재 덮임 상태를 바꿀 다음 정수 U
//         answer += count_slab(&tree, current_u, next_u - 1, n, m);  // 다음 경계 전까지 덮임이 일정한 정수 U 슬랩 합산
//         while (index < event_count && event[index].u == next_u) {  // 같은 U에서 생기는 덮임 추가와 제거를 모두 반영
//             change_cover(&tree, 1, 0, base, event[index].first, event[index].last, event[index].change);  // 해당 실패 V 구간의 덮임 수 증감
//             ++index;  // 다음 경계 이벤트로 이동
//         }  // 현재 U의 모든 실패 덮임 변경 완료
//         current_u = next_u;  // 새 덮임 상태에서 아직 세지 않은 첫 U 기록
//     }  // 모든 실패 사각형 경계 처리 끝
//     answer += count_slab(&tree, current_u, high_u, n, m);  // 마지막 이벤트 뒤에 남은 후보 U 슬랩 합산
//     free(nodes); free(coordinate); free(event);  // 덮임 트리와 압축 좌표, 이벤트 배열 해제
//     return answer;  // 모든 테스트 기록과 도로 경계를 만족하는 표지판 좌표 수 반환
// }  // 미로 주행 테스트 계수 끝
// 
// long long solution(int n, int m, int** tests, size_t tests_rows, size_t tests_cols) {  // 실제 C 입력 형식으로 표지판의 가능한 위치 수 계산
//     (void)tests_cols;  // 테스트 기록은 항상 네 정수이므로 열 수는 별도로 쓰지 않음
//     return solve_tests(n, m, tests, tests_rows);  // 성공 교집합과 실패 합집합 스윕의 결과 반환
// }  // C 풀이 진입점 끝

// 풀이 요약
// U=X+Y, V=X−Y로 바꾸면 맨해튼 거리 D 이하 조건이 U,V 각각 중심에서 D 이내인 사각형
// 성공 기록의 사각형은 교집합으로 모으고 실패 기록의 사각형 합집합은 U 스윕과 V 구간 덮임으로 제외
// 원래 도로 경계는 |V|≤U≤min(2N−V,2M+V), 정수 좌표 조건은 U와 V의 홀짝이 같다는 조건
// 실패 덮임이 일정한 U 슬랩마다 상·하한 식이 바뀌는 V 경계로 나누고 U 상한이 하한 이상인 범위만 남기기
// V=2t+p에서 허용 U 개수는 t의 일차식이므로 미덮임 V의 홀짝별 개수와 t 합만 조회해 격자점 수 합산
// 압축 리프의 일부만 조회되면 그 정수 구간의 개수와 합을 직접 계산; 음수 좌표의 나눗셈은 수학적 올림·내림으로 처리
// 테스트 수 Q에 대해 시간 O(Q log Q), 보조 공간 O(Q); 좌표 연산과 가능한 위치 수는 64비트 정수 사용
~~~

## 채점 기록

2026-10-24 사이트 채점: 정답 100/100. 1번째 제출에서 통과. C 제출 내역에서도 같은 날짜의 정답 기록 확인.

줄별 설명과 풀이 요약을 포함한 코드를 제출. 로컬 검사 횟수와 실행 시간은 사이트 채점 기록과 별도로 보관.
