// 자체 창작 연습 06 · 격자 통로의 최소 이동 
// 핵심 상태: dist[r][c]는 최소 이동 횟수이며 -1이면 미방문. 큐는 아직 이웃을 살피지 않은 칸이다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
#include <queue>
#include <string>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (string &s : grid) cin >> s;
    // n행 m열의 거리표를 -1로 초기화한다. 바깥 vector는 행, 안쪽 vector는 열이다.
    // queue<pair<int,int>>는 행·열 두 정수를 쌍으로 보관하는 선입선출 큐다.
    // grid는 문자열 행들의 vector다. grid[r][c]는 해당 칸의 문자 0 또는 1이다.
    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int,int>> q;
    int dr[4] = {-1,1,0,0}, dc[4] = {0,0,-1,1};
    // 시작이 통로면 거리 0을 기록하고 좌표 {0,0}을 큐에 넣는다.
    // 벽인 시작칸에서 탐색을 시작하면 잘못된 경로가 만들어질 수 있어 먼저 검사한다.
    // 모든 간선 비용이 1이므로 BFS의 처음 방문 거리가 최단 이동 횟수다.
    if (grid[0][0] == '1') {
        dist[0][0] = 0; q.push({0,0});
    }
    // q.front()로 앞의 좌표를 읽고 q.pop()으로 그 원소를 제거한다.
    // auto [r,c]는 pair를 행·열 변수로 나누는 C++17 구조적 바인딩이다.
    // empty인 큐에서 front나 pop을 쓰지 않도록 while 조건으로 보호한다.
    while (!q.empty()) {
        auto [r,c] = q.front(); q.pop();
        // 네 방향 이웃 좌표를 만든다. 범위 검사가 벽·방문 검사보다 먼저다.
        // continue는 이번 이웃만 건너뛰고 다음 방향을 검사하게 한다.
        // 처음 보는 통로는 현재 거리+1로 기록한 뒤 큐에 넣어 중복 방문을 막는다.
        for (int k = 0; k < 4; ++k) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m)
                continue;
            if (grid[nr][nc] == '0' || dist[nr][nc] != -1)
                continue;
            dist[nr][nc] = dist[r][c] + 1;  // 방문 표시와 거리 기록을 동시에 한다.
            q.push({nr,nc});
        }
    }
    cout << dist[n - 1][m - 1] << '\n';
}

// 복잡도: 시간 O(NM), 공간 O(NM). 각 칸은 최대 한 번 큐에 들어가고 네 이웃을 확인한다.
// 마지막 경계 확인:
// - 벽·범위 밖·방문한 칸을 모두 제외한다.
// - 방문 표시를 큐에서 꺼낼 때 하면 중복 삽입이 생긴다.
// - 이 문제는 지나간 칸 수가 아니라 이동 횟수다. 시작 거리는 0.
// - Python list.pop(0)은 앞 원소 이동 비용이 있으므로 deque.popleft를 쓴다.
