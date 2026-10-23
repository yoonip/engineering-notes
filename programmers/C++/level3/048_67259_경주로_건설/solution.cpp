#include <algorithm>
#include <array>
#include <functional>
#include <queue>
#include <tuple>
#include <vector>
using namespace std;

int solution(vector<vector<int>> board) {
    int n = (int)board.size(), dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    const int INF = 1000000000; vector<vector<array<int,4>>> distance(n, vector<array<int,4>>(n));
    for (auto& row : distance) for (auto& cell : row) cell.fill(INF);
    priority_queue<tuple<int,int,int,int>, vector<tuple<int,int,int,int>>, greater<tuple<int,int,int,int>>> heap;
    for (int d = 0; d < 4; ++d) { distance[0][0][d] = 0; heap.push({0,0,0,d}); }
    while (!heap.empty()) {
        auto [cost,r,c,old] = heap.top(); heap.pop();
        if (cost != distance[r][c][old]) continue;
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n || board[nr][nc]) continue;
            int candidate = cost + 100 + (d != old ? 500 : 0);
            if (candidate < distance[nr][nc][d]) { distance[nr][nc][d] = candidate; heap.push({candidate,nr,nc,d}); }
        }
    }
    return *min_element(distance[n - 1][n - 1].begin(), distance[n - 1][n - 1].end());
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <tuple>  // 여러 상태 값을 묶는 tuple
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> board) {  // 위치와 진입 방향별 최소 경주로 비용 계산
// int n = (int)board.size(), dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 보드 크기와 네 방향 이동량 선언
// const int INF = 1000000000; vector<vector<array<int,4>>> distance(n, vector<array<int,4>>(n));  // 위치와 진입 방향별 최소 건설 비용 저장
// for (auto& row : distance) for (auto& cell : row) cell.fill(INF);  // 아직 도달하지 않은 상태를 큰 값으로 초기화
// priority_queue<tuple<int,int,int,int>, vector<tuple<int,int,int,int>>, greater<tuple<int,int,int,int>>> heap;  // 비용이 작은 도로 상태부터 처리
// for (int d = 0; d < 4; ++d) { distance[0][0][d] = 0; heap.push({0,0,0,d}); }  // 첫 방향의 회전 비용을 없애도록 네 시작 방향 등록
// while (!heap.empty()) {  // 다익스트라 알고리즘으로 최소 비용 찾기
// auto [cost,r,c,old] = heap.top(); heap.pop();  // 현재 비용과 위치 및 이전 방향 꺼내기
// if (cost != distance[r][c][old]) continue;  // 오래된 비용 상태는 건너뛰기
// for (int d = 0; d < 4; ++d) {  // 네 방향으로 다음 칸 검사
// int nr = r + dr[d], nc = c + dc[d];  // 다음 좌표 계산
// if (nr < 0 || nr >= n || nc < 0 || nc >= n || board[nr][nc]) continue;  // 범위 밖과 벽을 제외
// int candidate = cost + 100 + (d != old ? 500 : 0);  // 직선 비용과 방향 전환의 코너 비용을 더하기
// if (candidate < distance[nr][nc][d]) { distance[nr][nc][d] = candidate; heap.push({candidate,nr,nc,d}); }  // 더 싼 건설 경로이면 갱신
// }  // 블록 끝
// }  // 블록 끝
// return *min_element(distance[n - 1][n - 1].begin(), distance[n - 1][n - 1].end());  // 도착점의 네 방향 중 최소 비용 반환
// }  // 블록 끝

// 풀이 요약
// 위치와 이동 방향을 상태로 직선 및 코너 비용을 더하는 다익스트라 탐색으로 최소 건설 비용 구하기
