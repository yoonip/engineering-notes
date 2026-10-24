#include <algorithm>
#include <string>
#include <vector>

using namespace std;
static constexpr int DR[4] = {-1, 1, 0, 0};
static constexpr int DC[4] = {0, 0, -1, 1};

static int bfs(const vector<string>& grid, int start, int blocked, vector<int>& distance, vector<int>* parent, vector<int>& queue) {
    int rows = static_cast<int>(grid.size()), columns = static_cast<int>(grid[0].size());
    fill(distance.begin(), distance.end(), -1);
    queue.clear();
    queue.push_back(start);
    distance[start] = 0;
    if (parent != nullptr) (*parent)[start] = -1;
    for (size_t head = 0; head < queue.size(); ++head) {
        int node = queue[head], row = node / columns, column = node % columns;
        for (int direction = 0; direction < 4; ++direction) {
            int nr = row + DR[direction], nc = column + DC[direction];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= columns) continue;
            int next = nr * columns + nc;
            if (next == blocked || grid[nr][nc] == '#' || distance[next] >= 0) continue;
            distance[next] = distance[node] + 1;
            if (parent != nullptr) (*parent)[next] = node;
            queue.push_back(next);
        }
    }
    return static_cast<int>(queue.size());
}

long long solution(vector<string> grid) {
    int rows = static_cast<int>(grid.size()), columns = static_cast<int>(grid[0].size());
    int cells = rows * columns;
    vector<int> starts, distance(cells), parent(cells), queue;
    vector<unsigned char> degree(cells);
    queue.reserve(cells);
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            if (grid[row][column] == '#') continue;
            int node = row * columns + column;
            if (grid[row][column] == 'o') starts.push_back(node);
            for (int direction = 0; direction < 4; ++direction) {
                int nr = row + DR[direction], nc = column + DC[direction];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && grid[nr][nc] != '#') ++degree[node];
            }
        }
    }
    int total = bfs(grid, starts[0], -1, distance, &parent, queue);
    int separation = distance[starts[1]];
    if (separation < 0) return 0;
    bool internal_branch = false;
    for (int node = parent[starts[1]]; node >= 0 && node != starts[0]; node = parent[node]) if (degree[node] >= 3) internal_branch = true;
    int nearest = cells + 1;
    int first_capacity = bfs(grid, starts[0], starts[1], distance, nullptr, queue);
    for (int node : queue) if (degree[node] >= 3) nearest = min(nearest, distance[node]);
    int second_capacity = bfs(grid, starts[1], starts[0], distance, nullptr, queue);
    for (int node : queue) if (degree[node] >= 3) nearest = min(nearest, distance[node]);
    int small_capacity = min(first_capacity, second_capacity), large_capacity = max(first_capacity, second_capacity);
    long long answer = 0;
    for (int head = 1; head * 2 <= total; ++head) {
        int body_limit = total - head;
        int basic_low = max(head, separation + 1 - head);
        int basic_high = min(large_capacity, body_limit);
        if (head <= small_capacity && basic_low <= basic_high) answer += basic_high - basic_low + 1;
        int flexible_low = body_limit + 1;
        if (internal_branch) flexible_low = max(head, separation + 2 - head);
        else if (nearest <= cells) flexible_low = max({head, nearest + 2, separation + nearest + 3 - head});
        if (flexible_low <= body_limit) {
            answer += body_limit - flexible_low + 1;
            int overlap_low = max(basic_low, flexible_low);
            if (head <= small_capacity && overlap_low <= basic_high) answer -= basic_high - overlap_low + 1;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 크기 구간의 하한·상한과 최근접 분기점 거리 비교
// #include <string>  // 격자 한 행을 담는 string
// #include <vector>  // 거리·부모·BFS 큐와 격자 배열
//
// using namespace std;  // 표준 라이브러리 이름 앞의 std:: 생략
// static constexpr int DR[4] = {-1, 1, 0, 0};  // 상하좌우 이동의 행 변화량
// static constexpr int DC[4] = {0, 0, -1, 1};  // 상하좌우 이동의 열 변화량
//
// static int bfs(const vector<string>& grid, int start, int blocked, vector<int>& distance, vector<int>* parent, vector<int>& queue) {  // 한 칸을 막거나 모두 열고 연결성분 크기와 거리 계산
//     int rows = static_cast<int>(grid.size()), columns = static_cast<int>(grid[0].size());  // 일차원 칸 번호를 행·열로 변환할 격자 크기
//     fill(distance.begin(), distance.end(), -1);  // 이번 BFS의 모든 칸을 미방문으로 초기화
//     queue.clear();  // 이전 BFS의 방문 순서 제거
//     queue.push_back(start);  // 시작점을 큐에 등록
//     distance[start] = 0;  // 시작점까지 거리는 0
//     if (parent != nullptr) (*parent)[start] = -1;  // 최단경로 복원이 필요한 호출에서 시작점의 부모를 비우기
//     for (size_t head = 0; head < queue.size(); ++head) {  // 뒤에 새 이웃을 붙이며 BFS 순서대로 처리
//         int node = queue[head], row = node / columns, column = node % columns;  // 현재 칸 번호와 행·열 좌표
//         for (int direction = 0; direction < 4; ++direction) {  // 상하좌우 이웃 네 칸 확인
//             int nr = row + DR[direction], nc = column + DC[direction];  // 다음 칸 좌표
//             if (nr < 0 || nr >= rows || nc < 0 || nc >= columns) continue;  // 격자 바깥 제외
//             int next = nr * columns + nc;  // 이웃 칸의 일차원 번호
//             if (next == blocked || grid[nr][nc] == '#' || distance[next] >= 0) continue;  // 고정 눈덩이·벽·이미 방문한 칸 제외
//             distance[next] = distance[node] + 1;  // 처음 도착한 최단거리 기록
//             if (parent != nullptr) (*parent)[next] = node;  // 초기 두 눈덩이 사이 경로 복원용 직전 칸 기록
//             queue.push_back(next);  // 이웃 칸도 방문 순서 뒤에 추가
//         }  // 현재 칸의 이웃 처리 끝
//     }  // 연결성분 탐색 끝
//     return static_cast<int>(queue.size());  // 방문한 칸 수가 연결성분 크기
// }  // BFS 함수 끝
//
// long long solution(vector<string> grid) {  // 만들 수 있는 머리·몸통 크기 쌍의 종류 수 반환
//     int rows = static_cast<int>(grid.size()), columns = static_cast<int>(grid[0].size());  // 격자의 행·열 수
//     int cells = rows * columns;  // 작업 배열의 전체 칸 수
//     vector<int> starts, distance(cells), parent(cells), queue;  // 두 초기 위치와 BFS의 거리·부모·방문 순서
//     vector<unsigned char> degree(cells);  // 각 칸의 벽 아닌 이웃 수는 최대 4
//     queue.reserve(cells);  // BFS를 반복해도 큐가 다시 할당되지 않게 용량 확보
//     for (int row = 0; row < rows; ++row) {  // 두 눈덩이와 그래프 차수 준비
//         for (int column = 0; column < columns; ++column) {  // 현재 행의 칸들 검사
//             if (grid[row][column] == '#') continue;  // 벽에는 눈덩이가 들어갈 수 없음
//             int node = row * columns + column;  // 현재 칸의 일차원 번호
//             if (grid[row][column] == 'o') starts.push_back(node);  // 초기 눈덩이 위치 저장
//             for (int direction = 0; direction < 4; ++direction) {  // 이동 가능한 이웃 수 확인
//                 int nr = row + DR[direction], nc = column + DC[direction];  // 이웃 좌표
//                 if (nr >= 0 && nr < rows && nc >= 0 && nc < columns && grid[nr][nc] != '#') ++degree[node];  // 격자 안의 벽 아닌 칸만 차수에 포함
//             }  // 현재 칸의 차수 계산 끝
//         }  // 현재 행 처리 끝
//     }  // 시작 위치와 차수 준비 끝
//     int total = bfs(grid, starts[0], -1, distance, &parent, queue);  // 두 눈덩이가 사용할 수 있는 연결성분의 전체 칸 수
//     int separation = distance[starts[1]];  // 초기 두 위치 사이 최단거리 D
//     if (separation < 0) return 0;  // 서로 만날 수 없는 입력이면 가능한 눈사람 없음
//     bool internal_branch = false;  // 초기 최단경로 내부에 다른 쪽으로 비켜설 칸이 있는지 표시
//     for (int node = parent[starts[1]]; node >= 0 && node != starts[0]; node = parent[node]) if (degree[node] >= 3) internal_branch = true;  // 양끝을 제외한 최단경로에서 차수 3 이상인 분기점 확인
//     int nearest = cells + 1;  // 분기점이 없는 경우를 나타내는 큰 거리
//     int first_capacity = bfs(grid, starts[0], starts[1], distance, nullptr, queue);  // 둘째를 고정했을 때 첫째가 혼자 모을 수 있는 최대 크기
//     for (int node : queue) if (degree[node] >= 3) nearest = min(nearest, distance[node]);  // 첫 시작점에서 도달하는 가장 가까운 분기점 후보
//     int second_capacity = bfs(grid, starts[1], starts[0], distance, nullptr, queue);  // 첫째를 고정했을 때 둘째가 혼자 모을 수 있는 최대 크기
//     for (int node : queue) if (degree[node] >= 3) nearest = min(nearest, distance[node]);  // 양쪽 후보를 합해 두 시작점에서의 최근접 분기점 거리 k 결정
//     int small_capacity = min(first_capacity, second_capacity), large_capacity = max(first_capacity, second_capacity);  // 머리와 몸통에 배정할 기본 크기 상한을 작은 값·큰 값으로 정리
//     long long answer = 0;  // 크기 쌍은 수백억 개가 될 수 있어 64비트로 합산
//     for (int head = 1; head * 2 <= total; ++head) {  // 머리 크기별로 가능한 몸통 구간을 세기
//         int body_limit = total - head;  // 눈은 한 번만 소비되므로 두 크기 합은 연결성분 크기 이하
//         int basic_low = max(head, separation + 1 - head);  // 몸통은 머리 이상이며 초기 두 칸을 연결할 D+1칸도 필요
//         int basic_high = min(large_capacity, body_limit);  // 기본 영역의 몸통 상한
//         if (head <= small_capacity && basic_low <= basic_high) answer += basic_high - basic_low + 1;  // 상대를 고정한 두 연결성분 크기로 만들 수 있는 기본 구간 합산
//         int flexible_low = body_limit + 1;  // 서로 비켜설 수 없는 경우 추가 구간은 비우기
//         if (internal_branch) flexible_low = max(head, separation + 2 - head);  // 경로 내부의 옆 칸 하나를 더 쓰면 Y가 완성되어 두 눈덩이 재배치 가능
//         else if (nearest <= cells) flexible_low = max({head, nearest + 2, separation + nearest + 3 - head});  // 끝 바깥 분기점은 몸통 k+2 이상·총합 D+k+3 이상이 되어야 재배치 가능
//         if (flexible_low <= body_limit) {  // 분기점으로 열리는 추가 몸통 구간이 있는 경우
//             answer += body_limit - flexible_low + 1;  // 이후 남은 눈을 어느 쪽에도 배정할 수 있는 구간 합산
//             int overlap_low = max(basic_low, flexible_low);  // 기본·추가 구간이 겹치기 시작하는 몸통 크기
//             if (head <= small_capacity && overlap_low <= basic_high) answer -= basic_high - overlap_low + 1;  // 같은 머리·몸통 쌍을 중복 합산한 부분은 한 번 빼기
//         }  // 현재 머리 크기의 추가 구간 처리 끝
//     }  // 모든 머리 크기 처리 끝
//     return answer;  // 위치와 무관하게 서로 다른 크기 쌍의 총수 반환
// }  // 지역 컨테이너는 호출이 끝나면 해제되어 다음 채점에 상태가 남지 않음

// 풀이 요약
// 두 눈덩이가 있는 연결성분 크기를 N, 초기 최단거리를 D로 두면 크기 합은 D+1 이상 N 이하. 머리 h는 몸통 b 이하.
// 상대 초기 칸을 막은 두 연결성분 크기를 C1,C2로 구함. h<=min(C1,C2), b<=max(C1,C2)이면 양쪽에서 눈을 모으는 기본 영역.
// 이미 눈을 치운 연결 영역에 Y 모양을 만들면 두 눈덩이의 위치를 새 눈 소비 없이 바꿀 수 있어, 남은 눈을 원하는 쪽에 배정 가능.
// 초기 최단경로 내부에 차수 3 이상 정점이 있으면 옆 칸 하나를 더 써 합 D+2부터 추가 영역이 열림.
// 내부 분기가 없을 때 두 초기점에서 최근접 차수 3 정점까지 거리를 k라 두면, 큰 눈덩이 크기 k+2 이상·합 D+k+3 이상에서 추가 영역이 열림. 분기점이 전혀 없으면 기본 영역만 사용.
// 각 머리 크기에서 기본 몸통 구간과 추가 구간의 합집합 길이를 세고, 겹친 부분은 빼기. BFS 세 번과 머리 크기 순회로 시간·공간 O(격자 칸 수).

