# 카드 짝 맞추기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/72415) · Level 3 · C++

## 풀이

남은 카드 상태별 일반 및 Ctrl 이동의 최단 거리를 구하고 카드 종류와 두 장을 선택하는 순서를 재귀적으로 최적화

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <functional>
#include <map>
#include <queue>
#include <vector>
using namespace std;

int solution(vector<vector<int>> board, int r, int c) {
    map<int,vector<int>> positions; int full = 0;
    for (int row = 0; row < 4; ++row) for (int col = 0; col < 4; ++col) if (board[row][col]) { positions[board[row][col]].push_back(row * 4 + col); full |= 1 << board[row][col]; }
    vector<array<int,16>> cached(128 * 16); vector<bool> ready(128 * 16, false);
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    auto distances = [&](int mask, int start) -> const array<int,16>& {
        int key = mask * 16 + start; auto& distance = cached[key];
        if (ready[key]) return distance; ready[key] = true; distance.fill(-1);
        queue<int> q; distance[start] = 0; q.push(start);
        while (!q.empty()) {
            int point = q.front(); q.pop(); int row = point / 4, col = point % 4;
            for (int d = 0; d < 4; ++d) {
                int nr = row + dr[d], nc = col + dc[d];
                if (nr >= 0 && nr < 4 && nc >= 0 && nc < 4) { int target = nr * 4 + nc; if (distance[target] == -1) { distance[target] = distance[point] + 1; q.push(target); } }
                nr = row; nc = col;
                while (nr + dr[d] >= 0 && nr + dr[d] < 4 && nc + dc[d] >= 0 && nc + dc[d] < 4) { nr += dr[d]; nc += dc[d]; int card = board[nr][nc]; if (card && (mask & (1 << card))) break; }
                int target = nr * 4 + nc; if (distance[target] == -1) { distance[target] = distance[point] + 1; q.push(target); }
            }
        }
        return distance;
    };
    vector<int> memo(128 * 16, -1);
    function<int(int,int)> solve = [&](int mask, int cursor) {
        if (mask == 0) return 0;
        int& best = memo[mask * 16 + cursor]; if (best != -1) return best; best = 1000000;
        const auto& start_distance = distances(mask, cursor);
        for (const auto& entry : positions) if (mask & (1 << entry.first)) {
            int first = entry.second[0], second = entry.second[1], remaining = mask ^ (1 << entry.first);
            int forward = start_distance[first] + distances(mask, first)[second] + 2 + solve(remaining, second);
            int backward = start_distance[second] + distances(mask, second)[first] + 2 + solve(remaining, first);
            best = min({best, forward, backward});
        }
        return best;
    };
    return solve(full, r * 4 + c);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <map>  // 키를 정렬해 보관하는 map
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> board, int r, int c) {  // 카드 제거 순서와 커서 이동을 함께 최적화
// map<int,vector<int>> positions; int full = 0;  // 카드 종류별 두 위치와 남은 카드 마스크 저장
// for (int row = 0; row < 4; ++row) for (int col = 0; col < 4; ++col) if (board[row][col]) { positions[board[row][col]].push_back(row * 4 + col); full |= 1 << board[row][col]; }  // 보드의 카드 위치 모으기
// vector<array<int,16>> cached(128 * 16); vector<bool> ready(128 * 16, false);  // 카드 상태와 시작점별 이동 거리를 기억
// int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 네 방향 이동량 선언
// auto distances = [&](int mask, int start) -> const array<int,16>& {  // 방향키와 Ctrl 방향키의 최단 거리 구하기
// int key = mask * 16 + start; auto& distance = cached[key];  // 현재 이동 거리 캐시를 참조
// if (ready[key]) return distance; ready[key] = true; distance.fill(-1);  // 계산한 상태는 재사용하고 새 상태 초기화
// queue<int> q; distance[start] = 0; q.push(start);  // 시작 커서 위치에서 너비 우선 탐색
// while (!q.empty()) {  // 키 입력 수가 작은 위치부터 처리
// int point = q.front(); q.pop(); int row = point / 4, col = point % 4;  // 현재 위치를 행과 열로 바꾸기
// for (int d = 0; d < 4; ++d) {  // 네 방향의 일반 및 Ctrl 이동 처리
// int nr = row + dr[d], nc = col + dc[d];  // 일반 방향키로 한 칸 이동한 위치
// if (nr >= 0 && nr < 4 && nc >= 0 && nc < 4) { int target = nr * 4 + nc; if (distance[target] == -1) { distance[target] = distance[point] + 1; q.push(target); } }  // 보드 안의 일반 이동 등록
// nr = row; nc = col;  // Ctrl 이동을 현재 위치에서 시작
// while (nr + dr[d] >= 0 && nr + dr[d] < 4 && nc + dc[d] >= 0 && nc + dc[d] < 4) { nr += dr[d]; nc += dc[d]; int card = board[nr][nc]; if (card && (mask & (1 << card))) break; }  // 남아 있는 첫 카드 또는 경계까지 이동
// int target = nr * 4 + nc; if (distance[target] == -1) { distance[target] = distance[point] + 1; q.push(target); }  // Ctrl 이동도 키 입력 한 번으로 등록
// }  // 블록 끝
// }  // 블록 끝
// return distance;  // 모든 칸까지의 최소 키 입력 수 반환
// };  // 블록 끝
// vector<int> memo(128 * 16, -1);  // 카드 집합과 커서 위치별 남은 최소 비용을 기억
// function<int(int,int)> solve = [&](int mask, int cursor) {  // 다음으로 제거할 카드 종류와 순서 선택
// if (mask == 0) return 0;  // 모든 카드를 제거하면 추가 입력이 없음
// int& best = memo[mask * 16 + cursor]; if (best != -1) return best; best = 1000000;  // 계산한 상태를 재사용하거나 최솟값 초기화
// const auto& start_distance = distances(mask, cursor);  // 현재 커서에서의 이동 거리 구하기
// for (const auto& entry : positions) if (mask & (1 << entry.first)) {  // 남은 카드 종류를 하나 고르기
// int first = entry.second[0], second = entry.second[1], remaining = mask ^ (1 << entry.first);  // 두 위치와 제거 후 카드 집합 구하기
// int forward = start_distance[first] + distances(mask, first)[second] + 2 + solve(remaining, second);  // 첫 카드부터 맞추는 이동과 Enter 두 번을 더하기
// int backward = start_distance[second] + distances(mask, second)[first] + 2 + solve(remaining, first);  // 반대 순서로 맞추는 비용도 계산
// best = min({best, forward, backward});  // 두 순서와 다른 카드 선택 중 최소 비용 고르기
// }  // 블록 끝
// return best;  // 현재 상태의 최소 키 입력 수 반환
// };  // 블록 끝
// return solve(full, r * 4 + c);  // 초기 카드 상태와 커서에서 시작
// }  // 블록 끝

// 풀이 요약
// 남은 카드 상태별 일반 및 Ctrl 이동의 최단 거리를 구하고 카드 종류와 두 장을 선택하는 순서를 재귀적으로 최적화
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/043_72415_%EC%B9%B4%EB%93%9C_%EC%A7%9D_%EB%A7%9E%EC%B6%94%EA%B8%B0/README.md)
