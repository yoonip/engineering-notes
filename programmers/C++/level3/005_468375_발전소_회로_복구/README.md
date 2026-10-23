# 발전소 회로 복구

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468375) · Level 3 · C++

## 풀이

패널 사이의 평면 및 승강기 이동 거리를 구하고 선행 복구 조건을 비트 마스크로 확인하며 최소 이동 비용을 메모이제이션

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cstdlib>
#include <functional>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

int solution(int h, vector<string> grid, vector<vector<int>> panels, vector<vector<int>> seqs) {
    (void)h;
    int n = (int)grid.size(), m = (int)grid[0].size(), k = (int)panels.size(), elevator = -1;
    const int INF = 1000000000;
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) if (grid[r][c] == '@') elevator = r * m + c;
    auto bfs = [&](int start) {
        vector<int> distance(n * m, INF); queue<int> q;
        distance[start] = 0; q.push(start);
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        while (!q.empty()) {
            int pos = q.front(); q.pop(); int r = pos / m, c = pos % m;
            for (int d = 0; d < 4; ++d) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= n || nc < 0 || nc >= m || grid[nr][nc] == '#') continue;
                int next = nr * m + nc;
                if (distance[next] == INF) { distance[next] = distance[pos] + 1; q.push(next); }
            }
        }
        return distance;
    };
    vector<int> positions; vector<vector<int>> distances;
    for (const auto& panel : panels) { positions.push_back((panel[1] - 1) * m + panel[2] - 1); distances.push_back(bfs(positions.back())); }
    vector<vector<int>> travel(k, vector<int>(k, 0));
    for (int i = 0; i < k; ++i) for (int j = 0; j < k; ++j) travel[i][j] = panels[i][0] == panels[j][0] ? distances[i][positions[j]] : distances[i][elevator] + abs(panels[i][0] - panels[j][0]) + distances[j][elevator];
    vector<int> required(k, 0);
    for (const auto& edge : seqs) required[edge[1] - 1] |= 1 << (edge[0] - 1);
    int full = (1 << k) - 1; unordered_map<long long, int> memo;
    function<int(int, int)> dfs = [&](int mask, int current) {
        if (mask == full) return 0;
        long long key = 1LL * mask * k + current;
        auto found = memo.find(key); if (found != memo.end()) return found->second;
        int answer = INF;
        for (int target = 0; target < k; ++target) {
            int bit = 1 << target;
            if ((mask & bit) || (required[target] & mask) != required[target]) continue;
            answer = min(answer, travel[current][target] + dfs(mask | bit, target));
        }
        return memo[key] = answer;
    };
    return dfs(required[0] == 0 ? 1 : 0, 0);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int h, vector<string> grid, vector<vector<int>> panels, vector<vector<int>> seqs) {  // 선행 복구 조건을 지키며 패널 이동 비용 최소화
// (void)h;  // 실제 층 이동은 패널의 층 번호 차이로 계산
// int n = (int)grid.size(), m = (int)grid[0].size(), k = (int)panels.size(), elevator = -1;  // 격자 및 패널 수와 승강기 위치 초기화
// const int INF = 1000000000;  // 도달할 수 없는 거리와 비용의 상한
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) if (grid[r][c] == '@') elevator = r * m + c;  // 승강기의 일차원 좌표 찾기
// auto bfs = [&](int start) {  // 같은 층의 모든 칸까지 최단 거리 구하기
// vector<int> distance(n * m, INF); queue<int> q;  // 거리 배열과 너비 우선 탐색 큐 만들기
// distance[start] = 0; q.push(start);  // 출발 칸을 거리 0으로 등록
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 상하좌우 이동량 선언
// while (!q.empty()) {  // 가까운 칸부터 처리
// int pos = q.front(); q.pop(); int r = pos / m, c = pos % m;  // 현재 위치를 행과 열로 복원
// for (int d = 0; d < 4; ++d) {  // 네 방향 이웃 검사
// int nr = r + dr[d], nc = c + dc[d];  // 이웃 좌표 계산
// if (nr < 0 || nr >= n || nc < 0 || nc >= m || grid[nr][nc] == '#') continue;  // 격자 밖과 벽을 제외
// int next = nr * m + nc;  // 이웃의 일차원 위치 구하기
// if (distance[next] == INF) { distance[next] = distance[pos] + 1; q.push(next); }  // 새 칸의 거리를 기록하고 큐에 넣기
// }  // 블록 끝
// }  // 블록 끝
// return distance;  // 출발 칸에서의 거리 배열 반환
// };  // 블록 끝
// vector<int> positions; vector<vector<int>> distances;  // 패널 좌표와 패널별 평면 거리 저장
// for (const auto& panel : panels) { positions.push_back((panel[1] - 1) * m + panel[2] - 1); distances.push_back(bfs(positions.back())); }  // 패널 좌표를 변환하고 거리 지도 계산
// vector<vector<int>> travel(k, vector<int>(k, 0));  // 패널 사이 이동 비용 저장
// for (int i = 0; i < k; ++i) for (int j = 0; j < k; ++j) travel[i][j] = panels[i][0] == panels[j][0] ? distances[i][positions[j]] : distances[i][elevator] + abs(panels[i][0] - panels[j][0]) + distances[j][elevator];  // 같은 층은 직접 이동하고 다른 층은 승강기를 경유
// vector<int> required(k, 0);  // 각 패널 전에 복구해야 하는 패널 집합 저장
// for (const auto& edge : seqs) required[edge[1] - 1] |= 1 << (edge[0] - 1);  // 선행 패널을 대상 패널의 비트 마스크에 넣기
// int full = (1 << k) - 1; unordered_map<long long, int> memo;  // 전체 복구 상태와 부분 상태의 최소 남은 비용 저장
// function<int(int, int)> dfs = [&](int mask, int current) {  // 복구한 패널 집합과 현재 위치로 최적 순서 탐색
// if (mask == full) return 0;  // 모든 패널을 복구하면 남은 이동 비용은 없음
// long long key = 1LL * mask * k + current;  // 상태를 정수 키 하나로 합치기
// auto found = memo.find(key); if (found != memo.end()) return found->second;  // 이미 계산한 상태는 재사용
// int answer = INF;  // 현재 상태의 최소 남은 비용 초기화
// for (int target = 0; target < k; ++target) {  // 다음으로 복구할 패널 고르기
// int bit = 1 << target;  // 대상 패널의 비트 구하기
// if ((mask & bit) || (required[target] & mask) != required[target]) continue;  // 이미 복구했거나 선행 조건이 부족하면 제외
// answer = min(answer, travel[current][target] + dfs(mask | bit, target));  // 이동 비용과 남은 최적 비용의 합 비교
// }  // 블록 끝
// return memo[key] = answer;  // 현재 상태의 최솟값을 기억하고 반환
// };  // 블록 끝
// return dfs(required[0] == 0 ? 1 : 0, 0);  // 1번 패널에서 시작하고 선행 조건이 없으면 즉시 복구한 것으로 두기
// }  // 블록 끝

// 풀이 요약
// 패널 사이의 평면 및 승강기 이동 거리를 구하고 선행 복구 조건을 비트 마스크로 확인하며 최소 이동 비용을 메모이제이션
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:28
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/005_468375_%EB%B0%9C%EC%A0%84%EC%86%8C_%ED%9A%8C%EB%A1%9C_%EB%B3%B5%EA%B5%AC/README.md)
