# 최고 속도

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468376) · Level 3 · C

## 풀이

모든 카메라 지점에서 도로를 자르고, 카메라가 없는 교점으로 이어진 조각은 서로소 집합으로 합치기; 카메라가 교점에 있어도 우회해 무료 통과하지 않도록 그 지점은 합치지 않음
카메라 간선만 남은 그래프에서 경로의 최소 제한을 최대화하는 우선순위 탐색을 하기; 도로 수 M에 대해 전처리 O(M² log M), 압축 그래프 공간 O(M)
예: 제한 80·70을 지나는 경로는 70까지 가능하며, 제한 45를 지나는 경로보다 좋음; 카메라 없는 연결 집합에 목적 도시가 있으면 0

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <stddef.h>

typedef struct { int x, y, limit; } Camera;
typedef struct { long long* cuts; int count, base; } Road;
typedef struct { int piece, camera; } Link;
typedef struct { int to, limit, next; } Edge;
typedef struct { int node, speed; } State;

static int compare_camera(const void* a, const void* b) {
    const Camera* x = a; const Camera* y = b;
    if (x->x != y->x) return (x->x > y->x) - (x->x < y->x);
    return (x->y > y->y) - (x->y < y->y);
}
static int compare_cut(const void* a, const void* b) {
    long long x = *(const long long*)a, y = *(const long long*)b;
    return (x > y) - (x < y);
}
static int find_root(int* parent, int node) {
    while (parent[node] != node) {
        parent[node] = parent[parent[node]];
        node = parent[node];
    }
    return node;
}
static int lower_cut(const Road* road, long long value) {
    int left = 0, right = road->count;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (road->cuts[mid] < value) left = mid + 1; else right = mid;
    }
    return left;
}
static int piece_at(const Road* road, long long value) {
    int index = lower_cut(road, value);
    if (index == road->count || road->cuts[index] > value) --index;
    if (index == road->count - 1) --index;
    return road->base + index;
}
static int camera_at(const Camera* camera, int count, int x, int y) {
    int left = 0, right = count;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (camera[mid].x < x || (camera[mid].x == x && camera[mid].y < y)) left = mid + 1; else right = mid;
    }
    return left < count && camera[left].x == x && camera[left].y == y;
}
static void heap_push(State* heap, int* count, State value) {
    int child = ++*count;
    while (child > 1 && heap[child / 2].speed < value.speed) {
        heap[child] = heap[child / 2]; child /= 2;
    }
    heap[child] = value;
}
static State heap_pop(State* heap, int* count) {
    State result = heap[1], last = heap[(*count)--];
    int parent = 1;
    while (parent * 2 <= *count) {
        int child = parent * 2;
        if (child < *count && heap[child + 1].speed > heap[child].speed) ++child;
        if (heap[child].speed <= last.speed) break;
        heap[parent] = heap[child]; parent = child;
    }
    if (*count) heap[parent] = last;
    return result;
}

int* solution(int** city, size_t city_rows, size_t city_cols, int** road, size_t road_rows, size_t road_cols) {
    int m = (int)road_rows, camera_count = 0, pieces = 0, link_count = 0;
    Camera* cameras = malloc((size_t)m * sizeof(Camera));
    for (int i = 0; i < m; ++i) cameras[i] = (Camera){(road[i][0] + road[i][2]) / 2, (road[i][1] + road[i][3]) / 2, road[i][4]};
    qsort(cameras, (size_t)m, sizeof(Camera), compare_camera);
    for (int i = 0; i < m; ++i) {
        if (camera_count && cameras[camera_count - 1].x == cameras[i].x && cameras[camera_count - 1].y == cameras[i].y) {
            if (cameras[i].limit < cameras[camera_count - 1].limit) cameras[camera_count - 1].limit = cameras[i].limit;
        } else cameras[camera_count++] = cameras[i];
    }
    size_t capacity = (size_t)m * (camera_count + 1);
    int* parent = malloc(capacity * sizeof(int));
    int* sizes = malloc(capacity * sizeof(int));
    Road* roads = calloc((size_t)m, sizeof(Road));
    Link* links = malloc((size_t)2 * m * camera_count * sizeof(Link));
    for (int i = 0; i < m; ++i) {
        Road* item = &roads[i];
        item->cuts = malloc((size_t)(camera_count + 2) * sizeof(long long));
        item->cuts[item->count++] = (long long)road[i][0] + road[i][1];
        item->cuts[item->count++] = (long long)road[i][2] + road[i][3];
        for (int j = 0; j < camera_count; ++j) {
            if (road[i][0] <= cameras[j].x && cameras[j].x <= road[i][2] && road[i][1] <= cameras[j].y && cameras[j].y <= road[i][3]) item->cuts[item->count++] = (long long)cameras[j].x + cameras[j].y;
        }
        qsort(item->cuts, (size_t)item->count, sizeof(long long), compare_cut);
        int unique = 0;
        for (int j = 0; j < item->count; ++j) if (!unique || item->cuts[j] != item->cuts[unique - 1]) item->cuts[unique++] = item->cuts[j];
        item->count = unique; item->base = pieces;
        for (int j = 1; j < unique; ++j) { parent[pieces] = pieces; sizes[pieces++] = 1; }
        for (int j = 0; j < camera_count; ++j) {
            if (road[i][0] > cameras[j].x || cameras[j].x > road[i][2] || road[i][1] > cameras[j].y || cameras[j].y > road[i][3]) continue;
            int index = lower_cut(item, (long long)cameras[j].x + cameras[j].y);
            if (index > 0) links[link_count++] = (Link){item->base + index - 1, j};
            if (index + 1 < unique) links[link_count++] = (Link){item->base + index, j};
        }
    }
    for (int i = 0; i < m; ++i) for (int j = 0; j < i; ++j) {
        int x = road[i][0] > road[j][0] ? road[i][0] : road[j][0];
        int y = road[i][1] > road[j][1] ? road[i][1] : road[j][1];
        if (x > road[i][2] || x > road[j][2] || y > road[i][3] || y > road[j][3] || camera_at(cameras, camera_count, x, y)) continue;
        int a = find_root(parent, piece_at(&roads[i], (long long)x + y));
        int b = find_root(parent, piece_at(&roads[j], (long long)x + y));
        if (a != b) {
            if (sizes[a] < sizes[b]) { int temporary = a; a = b; b = temporary; }
            parent[b] = a; sizes[a] += sizes[b];
        }
    }
    int nodes = pieces + camera_count, edge_count = 0;
    int* heads = malloc((size_t)nodes * sizeof(int));
    int* best = calloc((size_t)nodes, sizeof(int));
    Edge* edges = malloc((size_t)2 * link_count * sizeof(Edge));
    for (int i = 0; i < nodes; ++i) heads[i] = -1;
    for (int i = 0; i < link_count; ++i) {
        int a = find_root(parent, links[i].piece), b = pieces + links[i].camera, limit = cameras[links[i].camera].limit;
        edges[edge_count] = (Edge){b, limit, heads[a]}; heads[a] = edge_count++;
        edges[edge_count] = (Edge){a, limit, heads[b]}; heads[b] = edge_count++;
    }
    int* cities = malloc(city_rows * sizeof(int));
    for (size_t k = 0; k < city_rows; ++k) for (int i = 0; i < m; ++i) {
        if (road[i][0] <= city[k][0] && city[k][0] <= road[i][2] && road[i][1] <= city[k][1] && city[k][1] <= road[i][3]) {
            cities[k] = find_root(parent, piece_at(&roads[i], (long long)city[k][0] + city[k][1])); break;
        }
    }
    State* heap = malloc((size_t)(edge_count + 2) * sizeof(State));
    int heap_count = 0, infinity = 1000001;
    best[cities[0]] = infinity; heap_push(heap, &heap_count, (State){cities[0], infinity});
    while (heap_count) {
        State state = heap_pop(heap, &heap_count);
        if (state.speed != best[state.node]) continue;
        for (int e = heads[state.node]; e != -1; e = edges[e].next) {
            int speed = state.speed < edges[e].limit ? state.speed : edges[e].limit;
            if (speed > best[edges[e].to]) {
                best[edges[e].to] = speed; heap_push(heap, &heap_count, (State){edges[e].to, speed});
            }
        }
    }
    int* answer = malloc((city_rows - 1) * sizeof(int));
    for (size_t i = 1; i < city_rows; ++i) answer[i - 1] = best[cities[i]] == infinity ? 0 : best[cities[i]];
    for (int i = 0; i < m; ++i) free(roads[i].cuts);
    free(cameras); free(parent); free(sizes); free(roads); free(links);
    free(heads); free(best); free(edges); free(cities); free(heap);
    (void)city_cols; (void)road_cols;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stddef.h>  // 배열 크기를 나타내는 size_t
//
// typedef struct { int x, y, limit; } Camera;  // 교차점 x좌표 / 교차점 y좌표 / 현재 카메라의 제한 속도를 한 상태로 묶기
// typedef struct { long long* cuts; int count, base; } Road;  // 도로의 분할 좌표 목록과 조각 번호 시작점 보관
// typedef struct { int piece, camera; } Link;  // 도로 조각과 경계 카메라를 연결하는 항목
// typedef struct { int to, limit, next; } Edge;  // 현재 카메라의 제한 속도를 한 상태로 묶기
// typedef struct { int node, speed; } State;  // 다음 연결을 지난 뒤 가능한 속도를 한 상태로 묶기
//
// static int compare_camera(const void* a, const void* b) {  // 첫 조각 대표 / 둘째 조각 대표 계산용 함수
//     const Camera* x = a; const Camera* y = b;  // void 포인터를 카메라 구조체 포인터로 해석하기
//     if (x->x != y->x) return (x->x > y->x) - (x->x < y->x);  // x좌표가 다르면 x좌표 순서를 반환
//     return (x->y > y->y) - (x->y < y->y);  // 교차점 x좌표 / 교차점 y좌표로 최종값 계산
// }  // 이 범위 끝
// static int compare_cut(const void* a, const void* b) {  // 정수 경계를 오름차순으로 비교
//     long long x = *(const long long*)a, y = *(const long long*)b;  // 비교할 두 경계 값을 역참조하기
//     return (x > y) - (x < y);  // 교차점 x좌표 / 교차점 y좌표로 최종값 계산
// }  // 이 범위 끝
// static int find_root(int* parent, int node) {  // 연결 성분 대표를 찾으며 경로 압축
//     while (parent[node] != node) {  // 자기 자신이 대표가 될 때까지 부모를 따라가기
//         parent[node] = parent[parent[node]];  // 경로를 줄여 다음 탐색을 빠르게 하기
//         node = parent[node];  // 부모 정점으로 이동하기
//     }  // 이 범위 끝
//     return node;  // 경로 압축을 마친 연결 성분 대표 반환
// }  // 이 범위 끝
// static int lower_cut(const Road* road, long long value) {  // value 이상인 첫 경계의 인덱스를 찾기
//     int left = 0, right = road->count;  // 반열린 탐색 범위를 초기화
//     while (left < right) {  // 후보 범위가 남은 동안 반복하기
//         int mid = left + (right - left) / 2;  // 중간 카메라를 선택
//         if (road->cuts[mid] < value) left = mid + 1; else right = mid;  // 비교 결과에 따라 탐색 범위를 줄이기
//     }  // 이 범위 끝
//     return left;  // 해당 좌표가 속한 분할 구간의 경계 번호 반환
// }  // 이 범위 끝
// static int piece_at(const Road* road, long long value) {  // 카메라가 아닌 지점이 속한 도로 조각을 찾기
//     int index = lower_cut(road, value);  // 지점 이상인 첫 경계를 찾기
//     if (index == road->count || road->cuts[index] > value) --index;  // 경계 사이에 있으면 앞 경계의 조각을 선택
//     if (index == road->count - 1) --index;  // 마지막 끝점은 마지막 조각에 포함하기
//     return road->base + index;  // 카메라의 경계 위치로 최종값 계산
// }  // 이 범위 끝
// static int camera_at(const Camera* camera, int count, int x, int y) {  // 좌표에 카메라가 있는지 이진 탐색
//     int left = 0, right = count;  // 카메라 배열의 탐색 범위를 정하기
//     while (left < right) {  // 후보 범위가 남은 동안 반복하기
//         int mid = left + (right - left) / 2;  // 중간 카메라를 선택
//         if (camera[mid].x < x || (camera[mid].x == x && camera[mid].y < y)) left = mid + 1; else right = mid;  // 좌표의 사전식 순서로 범위를 줄이기
//     }  // 이 범위 끝
//     return left < count && camera[left].x == x && camera[left].y == y;  // 교차점 x좌표 / 교차점 y좌표로 최종값 계산
// }  // 이 범위 끝
// static void heap_push(State* heap, int* count, State value) {  // 속도가 가장 큰 상태를 먼저 꺼내는 힙에 삽입하기
//     int child = ++*count;  // 힙 뒤에 새 상태가 들어갈 위치를 만들기
//     while (child > 1 && heap[child / 2].speed < value.speed) {  // 부모보다 속도가 크면 위로 이동하기
//         heap[child] = heap[child / 2]; child /= 2;  // 부모 상태를 아래로 내리고 삽입 위치를 올리기
//     }  // 이 범위 끝
//     heap[child] = value;  // 올바른 위치에 새 상태를 저장
// }  // 이 범위 끝
// static State heap_pop(State* heap, int* count) {  // 현재 속도가 가장 큰 상태를 꺼내기
//     State result = heap[1], last = heap[(*count)--];  // 루트와 마지막 상태를 보관하고 크기를 줄이기
//     int parent = 1;  // 마지막 상태를 내릴 위치를 루트로 초기화
//     while (parent * 2 <= *count) {  // 자식 상태가 있으면 힙 순서를 복계산
//         int child = parent * 2;  // 왼쪽 자식을 선택
//         if (child < *count && heap[child + 1].speed > heap[child].speed) ++child;  // 두 자식 중 속도가 더 큰 쪽을 선택
//         if (heap[child].speed <= last.speed) break;  // 마지막 상태가 자식보다 크거나 같으면 이동을 끝
//         heap[parent] = heap[child]; parent = child;  // 자식을 올리고 빈 위치를 아래로 내리기
//     }  // 이 범위 끝
//     if (*count) heap[parent] = last;  // 남은 원소가 있으면 마지막 상태를 배치하기
//     return result;  // 최대 힙에서 가장 큰 제한값의 상태 반환
// }  // 이 범위 끝
//
// int* solution(int** city, size_t city_rows, size_t city_cols, int** road, size_t road_rows, size_t road_cols) {  // 모든 카메라 지점에서 도로를 자르고, 카메라가 없는 교점으로 이어진 조각은 서로소 집합으로 합치기; 카메라가 교점에 있어도 우회해 무료 통과하지 않도록 그 지점은 합치지 않음
//     int m = (int)road_rows, camera_count = 0, pieces = 0, link_count = 0;  // 도로 수와 각 자료구조의 크기를 초기화
//     Camera* cameras = malloc((size_t)m * sizeof(Camera));  // 도로마다 하나씩 카메라 정보를 저장할 공간을 확보하기
//     for (int i = 0; i < m; ++i) cameras[i] = (Camera){(road[i][0] + road[i][2]) / 2, (road[i][1] + road[i][3]) / 2, road[i][4]};  // 도로 중앙의 카메라 위치와 제한 속도를 계산
//     qsort(cameras, (size_t)m, sizeof(Camera), compare_camera);  // 같은 위치의 카메라가 이웃하도록 정렬
//     for (int i = 0; i < m; ++i) {  // 각 도로를 카메라가 없는 구간으로 나누기
//         if (camera_count && cameras[camera_count - 1].x == cameras[i].x && cameras[camera_count - 1].y == cameras[i].y) {  // 앞 카메라와 좌표가 같은지 확인
//             if (cameras[i].limit < cameras[camera_count - 1].limit) cameras[camera_count - 1].limit = cameras[i].limit;  // 같은 위치에서는 가장 엄격한 제한 속도를 남기기
//         } else cameras[camera_count++] = cameras[i];  // 새 위치의 카메라를 배열 앞쪽에 모으기
//     }  // 이 범위 끝
//     size_t capacity = (size_t)m * (camera_count + 1);  // 도로마다 생길 수 있는 조각 수의 상한을 계산
//     int* parent = malloc(capacity * sizeof(int));  // 각 조각의 분리 집합 부모를 저장
//     int* sizes = malloc(capacity * sizeof(int));  // 대표 집합의 크기를 저장
//     Road* roads = calloc((size_t)m, sizeof(Road));  // 도로별 경계 정보를 0으로 초기화
//     Link* links = malloc((size_t)2 * m * camera_count * sizeof(Link));  // 카메라 양쪽 도로 조각의 연결 공간을 확보하기
//     for (int i = 0; i < m; ++i) {  // 각 도로를 카메라가 없는 구간으로 나누기
//         Road* item = &roads[i];  // 현재 도로의 정보를 가리킴
//         item->cuts = malloc((size_t)(camera_count + 2) * sizeof(long long));  // 양 끝점과 카메라 경계를 담을 공간을 만들기
//         item->cuts[item->count++] = (long long)road[i][0] + road[i][1];  // 도로 시작점의 좌표 합을 경계로 넣기
//         item->cuts[item->count++] = (long long)road[i][2] + road[i][3];  // 도로 끝점의 좌표 합을 경계로 넣기
//         for (int j = 0; j < camera_count; ++j) {  // 도로 위 카메라와 양옆 조각의 연결을 기록
//             if (road[i][0] <= cameras[j].x && cameras[j].x <= road[i][2] && road[i][1] <= cameras[j].y && cameras[j].y <= road[i][3]) item->cuts[item->count++] = (long long)cameras[j].x + cameras[j].y;  // 선분에 포함된 카메라의 좌표 합을 경계로 넣기
//         }  // 이 범위 끝
//         qsort(item->cuts, (size_t)item->count, sizeof(long long), compare_cut);  // 경계를 도로를 따라 오름차순으로 정렬
//         int unique = 0;  // 서로 다른 경계 수를 초기화
//         for (int j = 0; j < item->count; ++j) if (!unique || item->cuts[j] != item->cuts[unique - 1]) item->cuts[unique++] = item->cuts[j];  // 중복 경계를 제거
//         item->count = unique; item->base = pieces;  // 정리한 경계 수와 현재 도로의 시작 조각 번호를 저장
//         for (int j = 1; j < unique; ++j) { parent[pieces] = pieces; sizes[pieces++] = 1; }  // 이웃 경계 사이마다 독립된 조각 집합을 만들기
//         for (int j = 0; j < camera_count; ++j) {  // 도로 위 카메라와 양옆 조각의 연결을 기록
//             if (road[i][0] > cameras[j].x || cameras[j].x > road[i][2] || road[i][1] > cameras[j].y || cameras[j].y > road[i][3]) continue;  // 현재 도로에 속하지 않는 카메라는 건너뛰기
//             int index = lower_cut(item, (long long)cameras[j].x + cameras[j].y);  // 카메라의 경계 인덱스를 찾기
//             if (index > 0) links[link_count++] = (Link){item->base + index - 1, j};  // 앞쪽 조각이 있으면 연결하기
//             if (index + 1 < unique) links[link_count++] = (Link){item->base + index, j};  // 뒤쪽 조각이 있으면 연결하기
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     for (int i = 0; i < m; ++i) for (int j = 0; j < i; ++j) {  // 모든 도로 쌍의 교차점을 확인
//         int x = road[i][0] > road[j][0] ? road[i][0] : road[j][0];  // 겹치는 좌표 범위의 왼쪽 경계를 계산
//         int y = road[i][1] > road[j][1] ? road[i][1] : road[j][1];  // 겹치는 좌표 범위의 아래쪽 경계를 계산
//         if (x > road[i][2] || x > road[j][2] || y > road[i][3] || y > road[j][3] || camera_at(cameras, camera_count, x, y)) continue;  // 만나지 않거나 카메라가 있는 교차점은 무료 연결하지 않음
//         int a = find_root(parent, piece_at(&roads[i], (long long)x + y));  // 첫 도로의 교차점 조각 대표를 찾기
//         int b = find_root(parent, piece_at(&roads[j], (long long)x + y));  // 둘째 도로의 교차점 조각 대표를 찾기
//         if (a != b) {  // 서로 다른 집합이면 카메라 없이 이동할 수 있는 구간으로 합치기
//             if (sizes[a] < sizes[b]) { int temporary = a; a = b; b = temporary; }  // 작은 집합을 큰 집합에 연결하기
//             parent[b] = a; sizes[a] += sizes[b];  // 대표와 집합 크기를 갱신
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     int nodes = pieces + camera_count, edge_count = 0;  // 조각 대표와 카메라로 이루어진 그래프 크기를 정하기
//     int* heads = malloc((size_t)nodes * sizeof(int));  // 각 정점의 첫 인접 간선 번호를 저장
//     int* best = calloc((size_t)nodes, sizeof(int));  // 정점마다 가능한 최고 속도를 0으로 초기화
//     Edge* edges = malloc((size_t)2 * link_count * sizeof(Edge));  // 양방향 연결에 필요한 간선 공간을 확보하기
//     for (int i = 0; i < nodes; ++i) heads[i] = -1;  // 모든 인접 리스트를 빈 상태로 초기화
//     for (int i = 0; i < link_count; ++i) {  // 카메라와 조각 사이의 양방향 간선을 만들기
//         int a = find_root(parent, links[i].piece), b = pieces + links[i].camera, limit = cameras[links[i].camera].limit;  // 양 끝 정점과 카메라의 제한 속도를 계산
//         edges[edge_count] = (Edge){b, limit, heads[a]}; heads[a] = edge_count++;  // 조각에서 카메라로 이동하는 간선을 추가하기
//         edges[edge_count] = (Edge){a, limit, heads[b]}; heads[b] = edge_count++;  // 카메라에서 조각으로 이동하는 간선을 추가하기
//     }  // 이 범위 끝
//     int* cities = malloc(city_rows * sizeof(int));  // 각 도시가 속한 무료 이동 구간의 대표를 저장
//     for (size_t k = 0; k < city_rows; ++k) for (int i = 0; i < m; ++i) {  // 도시를 지나는 첫 도로를 찾기
//         if (road[i][0] <= city[k][0] && city[k][0] <= road[i][2] && road[i][1] <= city[k][1] && city[k][1] <= road[i][3]) {  // 도시 좌표가 현재 도로 선분에 포함되는지 확인
//             cities[k] = find_root(parent, piece_at(&roads[i], (long long)city[k][0] + city[k][1])); break;  // 도시의 구간 대표를 저장하고 도로 탐색을 끝
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     State* heap = malloc((size_t)(edge_count + 2) * sizeof(State));  // 완화 성공 횟수의 상한에 맞게 최대 힙 공간을 확보하기
//     int heap_count = 0, infinity = 1000001;  // 빈 힙과 모든 카메라 제한보다 큰 시작 속도를 정하기
//     best[cities[0]] = infinity; heap_push(heap, &heap_count, (State){cities[0], infinity});  // 출발 도시의 구간에서 탐색을 시작하기
//     while (heap_count) {  // 처리할 경로 후보가 남은 동안 반복하기
//         State state = heap_pop(heap, &heap_count);  // 가능한 속도가 가장 큰 후보를 꺼내기
//         if (state.speed != best[state.node]) continue;  // 더 좋은 경로로 이미 갱신한 낡은 후보는 건너뛰기
//         for (int e = heads[state.node]; e != -1; e = edges[e].next) {  // 현재 정점에 연결된 모든 간선을 확인
//             int speed = state.speed < edges[e].limit ? state.speed : edges[e].limit;  // 경로와 새 카메라 제한 중 더 작은 값을 선택
//             if (speed > best[edges[e].to]) {  // 더 빠른 경로를 찾았는지 확인
//                 best[edges[e].to] = speed; heap_push(heap, &heap_count, (State){edges[e].to, speed});  // 최고 속도를 갱신하고 새 후보를 힙에 넣기
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     int* answer = malloc((city_rows - 1) * sizeof(int));  // 출발 도시에서 각 도시까지의 최고 속도 공간 확보
//     for (size_t i = 1; i < city_rows; ++i) answer[i - 1] = best[cities[i]] == infinity ? 0 : best[cities[i]];  // 카메라 없이 도달하면 0, 아니면 경로의 최고 속도를 저장
//     for (int i = 0; i < m; ++i) free(roads[i].cuts);  // 도로별 경계 배열을 해제
//     free(cameras); free(parent); free(sizes); free(roads); free(links);  // 도로 분할과 집합 병합에 사용한 메모리를 해제
//     free(heads); free(best); free(edges); free(cities); free(heap);  // 그래프와 탐색에 사용한 메모리를 해제
//     (void)city_cols; (void)road_cols;  // 고정된 열 개수 매개변수의 미사용을 명시하기
//     return answer;  // 출발 도시에서 각 도시까지의 최고 속도 반환
// }  // 이 범위 끝

// 풀이 요약
// 모든 카메라 지점에서 도로를 자르고, 카메라가 없는 교점으로 이어진 조각은 서로소 집합으로 합치기; 카메라가 교점에 있어도 우회해 무료 통과하지 않도록 그 지점은 합치지 않음
// 카메라 간선만 남은 그래프에서 경로의 최소 제한을 최대화하는 우선순위 탐색을 하기; 도로 수 M에 대해 전처리 O(M² log M), 압축 그래프 공간 O(M)
// 예: 제한 80·70을 지나는 경로는 70까지 가능하며, 제한 45를 지나는 경로보다 좋음; 카메라 없는 연결 집합에 목적 도시가 있으면 0
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:24:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/004_468376_%EC%B5%9C%EA%B3%A0_%EC%86%8D%EB%8F%84/README.md)
