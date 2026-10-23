#include <algorithm>
#include <array>
#include <queue>
#include <unordered_set>
#include <vector>
using namespace std;

int solution(vector<vector<int>> board) {
    int n = (int)board.size(), stride = n + 2;
    vector<vector<int>> grid(n + 2, vector<int>(n + 2, 1));
    for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) grid[r + 1][c + 1] = board[r][c];
    queue<array<int,3>> q; unordered_set<long long> visited;
    auto enqueue = [&](int first, int second, int time) {
        if (first > second) swap(first, second);
        long long key = 1LL * first * stride * stride + second;
        if (visited.insert(key).second) q.push({first,second,time});
    };
    enqueue(stride + 1, stride + 2, 0); int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (!q.empty()) {
        auto [first,second,time] = q.front(); q.pop();
        if (first == n * stride + n || second == n * stride + n) return time;
        int r1 = first / stride, c1 = first % stride, r2 = second / stride, c2 = second % stride;
        for (int d = 0; d < 4; ++d) if (!grid[r1 + dr[d]][c1 + dc[d]] && !grid[r2 + dr[d]][c2 + dc[d]]) enqueue(first + dr[d] * stride + dc[d], second + dr[d] * stride + dc[d], time + 1);
        if (r1 == r2) {
            for (int d : {-1,1}) if (!grid[r1 + d][c1] && !grid[r2 + d][c2]) { enqueue(first, first + d * stride, time + 1); enqueue(second, second + d * stride, time + 1); }
        } else {
            for (int d : {-1,1}) if (!grid[r1][c1 + d] && !grid[r2][c2 + d]) { enqueue(first, first + d, time + 1); enqueue(second, second + d, time + 1); }
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> board) {  // 로봇 두 끝점을 상태로 이동·회전 최단 경로 탐색
// int n = (int)board.size(), stride = n + 2;  // 격자 크기와 벽 테두리를 포함한 행 길이 구하기
// vector<vector<int>> grid(n + 2, vector<int>(n + 2, 1));  // 격자 바깥을 벽으로 둘러싸기
// for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) grid[r + 1][c + 1] = board[r][c];  // 원래 보드를 테두리 안으로 복사
// queue<array<int,3>> q; unordered_set<long long> visited;  // 로봇의 두 위치와 시간 및 방문 상태 저장
// auto enqueue = [&](int first, int second, int time) {  // 로봇 끝점 순서를 통일해 새 상태 등록
// if (first > second) swap(first, second);  // 회전 축 선택에 관계없이 같은 로봇 상태 합치기
// long long key = 1LL * first * stride * stride + second;  // 두 끝점 좌표를 하나의 키로 묶기
// if (visited.insert(key).second) q.push({first,second,time});  // 처음 방문한 상태만 큐에 넣기
// };  // 블록 끝
// enqueue(stride + 1, stride + 2, 0); int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 초기 가로 로봇과 네 방향 등록
// while (!q.empty()) {  // 이동 시간이 작은 상태부터 처리
// auto [first,second,time] = q.front(); q.pop();  // 현재 두 끝점과 이동 시간 꺼내기
// if (first == n * stride + n || second == n * stride + n) return time;  // 어느 끝점이든 목표에 닿으면 최소 시간 반환
// int r1 = first / stride, c1 = first % stride, r2 = second / stride, c2 = second % stride;  // 두 끝점을 행과 열로 바꾸기
// for (int d = 0; d < 4; ++d) if (!grid[r1 + dr[d]][c1 + dc[d]] && !grid[r2 + dr[d]][c2 + dc[d]]) enqueue(first + dr[d] * stride + dc[d], second + dr[d] * stride + dc[d], time + 1);  // 두 칸이 모두 빈 평행 이동 등록
// if (r1 == r2) {  // 가로 로봇은 위나 아래로 회전할 수 있음
// for (int d : {-1,1}) if (!grid[r1 + d][c1] && !grid[r2 + d][c2]) { enqueue(first, first + d * stride, time + 1); enqueue(second, second + d * stride, time + 1); }  // 회전 중 지나는 두 칸이 비면 두 축 회전 등록
// } else {  // 세로 로봇은 왼쪽이나 오른쪽으로 회전할 수 있음
// for (int d : {-1,1}) if (!grid[r1][c1 + d] && !grid[r2][c2 + d]) { enqueue(first, first + d, time + 1); enqueue(second, second + d, time + 1); }  // 두 끝점을 축으로 한 가로 회전 등록
// }  // 블록 끝
// }  // 블록 끝
// return -1;  // 목표에 도달할 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 로봇의 두 끝점 순서를 통일해 상태를 저장하고 가능한 평행 이동과 두 축 회전을 너비 우선 탐색
