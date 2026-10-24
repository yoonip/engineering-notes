#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static const int DR[4] = {-1, 1, 0, 0};
static const int DC[4] = {0, 0, -1, 1};
static int larger(int a, int b) { return a > b ? a : b; }
static int smaller(int a, int b) { return a < b ? a : b; }

static int bfs(const char* grid[], int rows, int columns, int start, int blocked, int distance[], int parent[], int queue[]) {
    int cells = rows * columns;
    for (int i = 0; i < cells; ++i) distance[i] = -1;
    int head = 0, tail = 1;
    queue[0] = start;
    distance[start] = 0;
    if (parent != NULL) parent[start] = -1;
    while (head < tail) {
        int node = queue[head++];
        int row = node / columns, column = node % columns;
        for (int direction = 0; direction < 4; ++direction) {
            int nr = row + DR[direction], nc = column + DC[direction];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= columns) continue;
            int next = nr * columns + nc;
            if (next == blocked || grid[nr][nc] == '#' || distance[next] >= 0) continue;
            distance[next] = distance[node] + 1;
            if (parent != NULL) parent[next] = node;
            queue[tail++] = next;
        }
    }
    return tail;
}

long long solution(const char* grid[], size_t grid_len) {
    int rows = (int)grid_len, columns = (int)strlen(grid[0]);
    int cells = rows * columns;
    int* storage = malloc((size_t)cells * 3 * sizeof(*storage));
    int* distance = storage;
    int* parent = distance + cells;
    int* queue = parent + cells;
    unsigned char* degree = calloc((size_t)cells, sizeof(*degree));
    int starts[2], found = 0;
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            if (grid[row][column] == '#') continue;
            int node = row * columns + column;
            if (grid[row][column] == 'o') starts[found++] = node;
            for (int direction = 0; direction < 4; ++direction) {
                int nr = row + DR[direction], nc = column + DC[direction];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && grid[nr][nc] != '#') ++degree[node];
            }
        }
    }
    int total = bfs(grid, rows, columns, starts[0], -1, distance, parent, queue);
    int separation = distance[starts[1]];
    if (separation < 0) { free(degree); free(storage); return 0; }
    int internal_branch = 0;
    for (int node = parent[starts[1]]; node >= 0 && node != starts[0]; node = parent[node]) {
        if (degree[node] >= 3) internal_branch = 1;
    }
    int nearest = cells + 1;
    int first_capacity = bfs(grid, rows, columns, starts[0], starts[1], distance, NULL, queue);
    for (int i = 0; i < first_capacity; ++i) if (degree[queue[i]] >= 3) nearest = smaller(nearest, distance[queue[i]]);
    int second_capacity = bfs(grid, rows, columns, starts[1], starts[0], distance, NULL, queue);
    for (int i = 0; i < second_capacity; ++i) if (degree[queue[i]] >= 3) nearest = smaller(nearest, distance[queue[i]]);
    int small_capacity = smaller(first_capacity, second_capacity);
    int large_capacity = larger(first_capacity, second_capacity);
    long long answer = 0;
    for (int head = 1; head * 2 <= total; ++head) {
        int body_limit = total - head;
        int basic_low = larger(head, separation + 1 - head);
        int basic_high = smaller(large_capacity, body_limit);
        if (head <= small_capacity && basic_low <= basic_high) answer += basic_high - basic_low + 1;
        int flexible_low = body_limit + 1;
        if (internal_branch) flexible_low = larger(head, separation + 2 - head);
        else if (nearest <= cells) flexible_low = larger(larger(head, nearest + 2), separation + nearest + 3 - head);
        if (flexible_low <= body_limit) {
            answer += body_limit - flexible_low + 1;
            int overlap_low = larger(basic_low, flexible_low);
            if (head <= small_capacity && overlap_low <= basic_high) answer -= basic_high - overlap_low + 1;
        }
    }
    free(degree);
    free(storage);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 격자 행 수를 받을 size_t
// #include <stdlib.h>  // BFS 작업 배열 할당·해제
// #include <string.h>  // 첫 행 문자열로 열 수를 구할 strlen
//
// static const int DR[4] = {-1, 1, 0, 0};  // 상하좌우 이동의 행 변화량
// static const int DC[4] = {0, 0, -1, 1};  // 상하좌우 이동의 열 변화량
// static int larger(int a, int b) { return a > b ? a : b; }  // 조건 연산자로 몸통 크기의 여러 하한 중 큰 값 선택
// static int smaller(int a, int b) { return a < b ? a : b; }  // 조건 연산자로 몸통 크기의 여러 상한 중 작은 값 선택
//
// static int bfs(const char* grid[], int rows, int columns, int start, int blocked, int distance[], int parent[], int queue[]) {  // 한 칸을 막거나 전체를 열고 시작점에서의 거리·연결성분 계산
//     int cells = rows * columns;  // 격자 좌표를 일차원 번호로 바꿀 전체 칸 수
//     for (int i = 0; i < cells; ++i) distance[i] = -1;  // -1은 이번 BFS에서 아직 방문하지 않은 칸
//     int head = 0, tail = 1;  // 배열 큐의 읽을 위치와 다음에 넣을 위치
//     queue[0] = start;  // 시작점을 큐에 등록
//     distance[start] = 0;  // 시작점까지 거리는 0
//     if (parent != NULL) parent[start] = -1;  // 최단경로 복원이 필요한 호출에서는 시작점의 부모를 비우기
//     while (head < tail) {  // 도달 가능한 모든 벽 아닌 칸 탐색
//         int node = queue[head++];  // 다음에 이웃을 살펴볼 칸
//         int row = node / columns, column = node % columns;  // 일차원 번호를 행·열 좌표로 복원
//         for (int direction = 0; direction < 4; ++direction) {  // 상하좌우 이웃 네 칸 검사
//             int nr = row + DR[direction], nc = column + DC[direction];  // 인접 칸의 행·열
//             if (nr < 0 || nr >= rows || nc < 0 || nc >= columns) continue;  // 격자 바깥으로는 이동 불가
//             int next = nr * columns + nc;  // 이웃 칸의 일차원 번호
//             if (next == blocked || grid[nr][nc] == '#' || distance[next] >= 0) continue;  // 막아 둔 눈덩이·벽·이미 방문한 칸 제외
//             distance[next] = distance[node] + 1;  // BFS에서 처음 도착한 거리가 최단거리
//             if (parent != NULL) parent[next] = node;  // 초기 두 눈덩이 사이 최단경로를 복원할 직전 칸 기록
//             queue[tail++] = next;  // 이웃 칸도 다음 탐색에 추가
//         }  // 현재 칸의 이웃 처리 끝
//     }  // 연결성분 탐색 끝
//     return tail;  // 방문한 칸 수가 이 시작점의 연결성분 크기
// }  // BFS 함수 끝
//
// long long solution(const char* grid[], size_t grid_len) {  // 만들 수 있는 머리·몸통 크기 쌍의 종류 수 반환
//     int rows = (int)grid_len, columns = (int)strlen(grid[0]);  // 격자의 행·열 수
//     int cells = rows * columns;  // 작업 배열에 필요한 전체 칸 수
//     int* storage = malloc((size_t)cells * 3 * sizeof(*storage));  // 거리·부모·큐를 한 번에 할당
//     int* distance = storage;  // 현재 BFS의 거리 배열
//     int* parent = distance + cells;  // 처음 구한 최단경로의 직전 칸 배열
//     int* queue = parent + cells;  // 각 BFS의 방문 순서를 담을 배열 큐
//     unsigned char* degree = calloc((size_t)cells, sizeof(*degree));  // 각 칸의 벽 아닌 이웃 수는 최대 4라 한 바이트로 저장
//     int starts[2], found = 0;  // 크기 1인 두 눈덩이의 초기 칸
//     for (int row = 0; row < rows; ++row) {  // 초기 눈덩이와 격자 그래프의 차수 확인
//         for (int column = 0; column < columns; ++column) {  // 현재 행의 모든 칸 검사
//             if (grid[row][column] == '#') continue;  // 벽에는 눈덩이가 들어갈 수 없음
//             int node = row * columns + column;  // 현재 칸의 일차원 번호
//             if (grid[row][column] == 'o') starts[found++] = node;  // 두 시작 위치 기록
//             for (int direction = 0; direction < 4; ++direction) {  // 벽 아닌 인접 칸 수 세기
//                 int nr = row + DR[direction], nc = column + DC[direction];  // 이웃 좌표
//                 if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && grid[nr][nc] != '#') ++degree[node];  // 실제로 이동할 수 있는 이웃만 차수에 포함
//             }  // 현재 칸의 차수 계산 끝
//         }  // 현재 행 처리 끝
//     }  // 시작 위치와 차수 준비 끝
//     int total = bfs(grid, rows, columns, starts[0], -1, distance, parent, queue);  // 두 눈덩이가 있는 연결성분의 전체 사용 가능 칸 수
//     int separation = distance[starts[1]];  // 초기 두 위치 사이 최단거리 D
//     if (separation < 0) { free(degree); free(storage); return 0; }  // 서로 만날 수 없는 입력이면 가능한 눈사람 없음
//     int internal_branch = 0;  // 초기 최단경로 내부에 옆으로 비켜설 분기점이 있는지 표시
//     for (int node = parent[starts[1]]; node >= 0 && node != starts[0]; node = parent[node]) {  // 양끝을 제외한 초기 최단경로의 칸들만 검사
//         if (degree[node] >= 3) internal_branch = 1;  // 경로의 앞뒤 외에 다른 이웃이 있으면 내부 분기점
//     }  // 초기 경로의 내부 분기 여부 확인 끝
//     int nearest = cells + 1;  // 분기점이 없을 때는 도달 불가를 나타낼 큰 거리
//     int first_capacity = bfs(grid, rows, columns, starts[0], starts[1], distance, NULL, queue);  // 둘째 눈덩이를 고정했을 때 첫째가 혼자 모을 수 있는 최대 크기
//     for (int i = 0; i < first_capacity; ++i) if (degree[queue[i]] >= 3) nearest = smaller(nearest, distance[queue[i]]);  // 첫 시작점 쪽에서 가장 가까운 분기점 거리 후보
//     int second_capacity = bfs(grid, rows, columns, starts[1], starts[0], distance, NULL, queue);  // 첫째 눈덩이를 고정했을 때 둘째가 혼자 모을 수 있는 최대 크기
//     for (int i = 0; i < second_capacity; ++i) if (degree[queue[i]] >= 3) nearest = smaller(nearest, distance[queue[i]]);  // 다른 시작점에서도 확인해 두 점 전체의 가장 가까운 분기점 거리 k 결정
//     int small_capacity = smaller(first_capacity, second_capacity);  // 작은 눈덩이에 배정할 수 있는 기본 크기 상한
//     int large_capacity = larger(first_capacity, second_capacity);  // 큰 눈덩이에 배정할 수 있는 기본 크기 상한
//     long long answer = 0;  // 머리 이하 몸통 크기 쌍은 많으면 수백억 개라 64비트로 합산
//     for (int head = 1; head * 2 <= total; ++head) {  // 머리보다 몸통이 작지 않도록 머리 크기별로 세기
//         int body_limit = total - head;  // 눈 한 칸은 한 번만 커지게 하므로 두 크기 합은 전체 칸 수 이하
//         int basic_low = larger(head, separation + 1 - head);  // 몸통은 머리 이상이고 두 초기점을 연결할 D+1칸도 필요
//         int basic_high = smaller(large_capacity, body_limit);  // 고정된 상대를 넘지 않는 기본 영역의 몸통 상한
//         if (head <= small_capacity && basic_low <= basic_high) answer += basic_high - basic_low + 1;  // 두 시작점 쪽에서 각각 확보할 수 있는 기본 구간 합산
//         int flexible_low = body_limit + 1;  // 눈덩이를 서로 비켜 줄 수 없다면 추가 구간은 비워 두기
//         if (internal_branch) flexible_low = larger(head, separation + 2 - head);  // 경로 내부 분기점은 옆 칸 하나를 더 쓰면 Y가 완성되어 자유롭게 재배치 가능
//         else if (nearest <= cells) flexible_low = larger(larger(head, nearest + 2), separation + nearest + 3 - head);  // 끝 바깥 분기점은 큰 눈덩이가 k+2 이상이고 합이 D+k+3 이상이어야 서로 비켜설 수 있음
//         if (flexible_low <= body_limit) {  // 분기점을 이용해 추가로 만들 수 있는 몸통 구간이 있는 경우
//             answer += body_limit - flexible_low + 1;  // 재배치 후 남은 눈을 어느 쪽에도 줄 수 있는 구간 합산
//             int overlap_low = larger(basic_low, flexible_low);  // 기본 구간과 추가 구간이 겹치기 시작하는 몸통 크기
//             if (head <= small_capacity && overlap_low <= basic_high) answer -= basic_high - overlap_low + 1;  // 같은 머리·몸통 쌍을 두 번 센 겹친 부분은 한 번 빼기
//         }  // 현재 머리 크기의 추가 구간 처리 끝
//     }  // 모든 머리 크기 처리 끝
//     free(degree);  // 차수 배열 해제
//     free(storage);  // BFS 작업 공간 해제
//     return answer;  // 위치가 아닌 크기 쌍으로 구분한 눈사람 종류 수 반환
// }  // solution 함수 끝

// 풀이 요약
// 두 눈덩이가 있는 연결성분 크기를 N, 초기 최단거리를 D로 두면 크기 합은 D+1 이상 N 이하. 머리 h는 몸통 b 이하.
// 상대 초기 칸을 막은 두 연결성분 크기를 C1,C2로 구함. h<=min(C1,C2), b<=max(C1,C2)이면 양쪽에서 눈을 모으는 기본 영역.
// 이미 눈을 치운 연결 영역에 Y 모양을 만들면 두 눈덩이의 위치를 새 눈 소비 없이 바꿀 수 있어, 남은 눈을 원하는 쪽에 배정 가능.
// 초기 최단경로 내부에 차수 3 이상 정점이 있으면 옆 칸 하나를 더 써 합 D+2부터 추가 영역이 열림.
// 내부 분기가 없을 때 두 초기점에서 최근접 차수 3 정점까지 거리를 k라 두면, 큰 눈덩이 크기 k+2 이상·합 D+k+3 이상에서 추가 영역이 열림. 분기점이 전혀 없으면 기본 영역만 사용.
// 각 머리 크기에서 기본 몸통 구간과 추가 구간의 합집합 길이를 세고, 겹친 부분은 빼기. BFS 세 번과 머리 크기 순회로 시간·공간 O(격자 칸 수).

