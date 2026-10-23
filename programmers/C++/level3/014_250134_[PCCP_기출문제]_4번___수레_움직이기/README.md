# [PCCP 기출문제] 4번 / 수레 움직이기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250134) · Level 3 · C++

## 풀이

두 수레의 위치와 개별 방문 칸을 상태로 동시에 이동시키며 충돌, 자리 교환, 재방문을 제외하고 거리 하한으로 가지치기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <cstdlib>
#include <functional>
#include <unordered_map>
#include <vector>
using namespace std;

int solution(vector<vector<int>> maze) {
    int n = (int)maze.size(), m = (int)maze[0].size(), size = n * m;
    int locations[5]{}; vector<vector<int>> neighbors(size);
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) {
        int pos = r * m + c;
        if (maze[r][c] >= 1 && maze[r][c] <= 4) locations[maze[r][c]] = pos;
        for (int d = 0; d < 4; ++d) { int nr = r + dr[d], nc = c + dc[d]; if (nr >= 0 && nr < n && nc >= 0 && nc < m && maze[nr][nc] != 5) neighbors[pos].push_back(nr * m + nc); }
    }
    int red_goal = locations[3], blue_goal = locations[4], answer = size + 1;
    vector<int> red_distance(size), blue_distance(size);
    for (int pos = 0; pos < size; ++pos) { red_distance[pos] = abs(pos / m - red_goal / m) + abs(pos % m - red_goal % m); blue_distance[pos] = abs(pos / m - blue_goal / m) + abs(pos % m - blue_goal % m); }
    unordered_map<unsigned long long, int> seen;
    function<void(int, int, int, int, int)> dfs = [&](int red, int blue, int red_mask, int blue_mask, int turns) {
        if (red == red_goal && blue == blue_goal) { answer = min(answer, turns); return; }
        if (turns + max(red_distance[red], blue_distance[blue]) >= answer) return;
        unsigned long long key = red | (1ULL * blue << 4) | (1ULL * red_mask << 8) | (1ULL * blue_mask << 24);
        auto found = seen.find(key); if (found != seen.end() && found->second <= turns) return;
        seen[key] = turns;
        vector<int> reds, blues;
        if (red == red_goal) reds.push_back(red); else for (int pos : neighbors[red]) if (!(red_mask & (1 << pos))) reds.push_back(pos);
        if (blue == blue_goal) blues.push_back(blue); else for (int pos : neighbors[blue]) if (!(blue_mask & (1 << pos))) blues.push_back(pos);
        sort(reds.begin(), reds.end(), [&](int a, int b) { return red_distance[a] < red_distance[b]; });
        sort(blues.begin(), blues.end(), [&](int a, int b) { return blue_distance[a] < blue_distance[b]; });
        for (int next_red : reds) for (int next_blue : blues) {
            if (next_red == next_blue || (next_red == blue && next_blue == red)) continue;
            dfs(next_red, next_blue, red_mask | (1 << next_red), blue_mask | (1 << next_blue), turns + 1);
        }
    };
    dfs(locations[1], locations[2], 1 << locations[1], 1 << locations[2], 0);
    return answer == size + 1 ? 0 : answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <cstdlib>  // 정수 절댓값 같은 기본 유틸리티
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> maze) {  // 두 수레의 방문 기록을 나눠 최소 동시 이동 찾기
// int n = (int)maze.size(), m = (int)maze[0].size(), size = n * m;  // 미로의 크기 구하기
// int locations[5]{}; vector<vector<int>> neighbors(size);  // 두 수레의 출발 및 도착 위치와 인접 칸 저장
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 상하좌우 이동량 선언
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) {  // 모든 위치의 상태와 이동 가능 이웃 구하기
// int pos = r * m + c;  // 일차원 위치 구하기
// if (maze[r][c] >= 1 && maze[r][c] <= 4) locations[maze[r][c]] = pos;  // 수레와 목표 위치 저장
// for (int d = 0; d < 4; ++d) { int nr = r + dr[d], nc = c + dc[d]; if (nr >= 0 && nr < n && nc >= 0 && nc < m && maze[nr][nc] != 5) neighbors[pos].push_back(nr * m + nc); }  // 벽이 아닌 이웃 칸 등록
// }  // 블록 끝
// int red_goal = locations[3], blue_goal = locations[4], answer = size + 1;  // 두 도착점과 최소 이동 수 초기화
// vector<int> red_distance(size), blue_distance(size);  // 가지치기에 사용할 목표까지의 맨해튼 거리 저장
// for (int pos = 0; pos < size; ++pos) { red_distance[pos] = abs(pos / m - red_goal / m) + abs(pos % m - red_goal % m); blue_distance[pos] = abs(pos / m - blue_goal / m) + abs(pos % m - blue_goal % m); }  // 각 칸에서 두 목표까지의 거리 하한 구하기
// unordered_map<unsigned long long, int> seen;  // 동일 상태에 도착한 최소 턴 수를 기억
// function<void(int, int, int, int, int)> dfs = [&](int red, int blue, int red_mask, int blue_mask, int turns) {  // 두 수레의 위치와 개별 방문 집합으로 탐색
// if (red == red_goal && blue == blue_goal) { answer = min(answer, turns); return; }  // 두 수레가 모두 도착하면 최솟값 갱신
// if (turns + max(red_distance[red], blue_distance[blue]) >= answer) return;  // 거리 하한으로도 현재 최선을 줄일 수 없으면 가지치기
// unsigned long long key = red | (1ULL * blue << 4) | (1ULL * red_mask << 8) | (1ULL * blue_mask << 24);  // 최대 16칸의 전체 상태를 하나의 정수로 묶기
// auto found = seen.find(key); if (found != seen.end() && found->second <= turns) return;  // 같거나 적은 턴으로 이미 방문한 상태는 제외
// seen[key] = turns;  // 현재 상태의 도착 턴 기록
// vector<int> reds, blues;  // 이번 턴의 두 수레 이동 후보 저장
// if (red == red_goal) reds.push_back(red); else for (int pos : neighbors[red]) if (!(red_mask & (1 << pos))) reds.push_back(pos);  // 도착한 빨간 수레는 멈추고 아니면 미방문 이웃으로 가기
// if (blue == blue_goal) blues.push_back(blue); else for (int pos : neighbors[blue]) if (!(blue_mask & (1 << pos))) blues.push_back(pos);  // 파란 수레에도 같은 개별 방문 규칙 적용
// sort(reds.begin(), reds.end(), [&](int a, int b) { return red_distance[a] < red_distance[b]; });  // 목표와 가까운 후보를 먼저 탐색
// sort(blues.begin(), blues.end(), [&](int a, int b) { return blue_distance[a] < blue_distance[b]; });  // 파란 수레도 거리순으로 탐색
// for (int next_red : reds) for (int next_blue : blues) {  // 두 수레의 동시 이동 조합 검사
// if (next_red == next_blue || (next_red == blue && next_blue == red)) continue;  // 같은 칸 도착과 두 수레의 자리 교환을 제외
// dfs(next_red, next_blue, red_mask | (1 << next_red), blue_mask | (1 << next_blue), turns + 1);  // 개별 방문을 반영하고 다음 턴 탐색
// }  // 블록 끝
// };  // 블록 끝
// dfs(locations[1], locations[2], 1 << locations[1], 1 << locations[2], 0);  // 두 출발 칸을 방문한 상태로 시작
// return answer == size + 1 ? 0 : answer;  // 두 수레를 모두 보낼 수 없으면 0 반환
// }  // 블록 끝

// 풀이 요약
// 두 수레의 위치와 개별 방문 칸을 상태로 동시에 이동시키며 충돌, 자리 교환, 재방문을 제외하고 거리 하한으로 가지치기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/014_250134_%5BPCCP_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_4%EB%B2%88___%EC%88%98%EB%A0%88_%EC%9B%80%EC%A7%81%EC%9D%B4%EA%B8%B0/README.md)
