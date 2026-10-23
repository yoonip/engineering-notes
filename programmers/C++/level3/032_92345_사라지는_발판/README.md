# 사라지는 발판

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92345) · Level 3 · C++

## 풀이

남은 발판과 두 플레이어 위치를 상태로 최적 게임을 재귀 탐색하며 이길 때는 가장 빨리, 질 때는 가장 늦게 끝나는 수 고르기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<vector<int>> board, vector<int> aloc, vector<int> bloc) {
    int n = (int)board.size(), m = (int)board[0].size(), mask = 0;
    vector<vector<int>> neighbors(n * m); int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) {
        int pos = r * m + c; if (board[r][c]) mask |= 1 << pos;
        for (int d = 0; d < 4; ++d) { int nr = r + dr[d], nc = c + dc[d]; if (nr >= 0 && nr < n && nc >= 0 && nc < m) neighbors[pos].push_back(nr * m + nc); }
    }
    unordered_map<unsigned long long, pair<bool, int>> memo;
    function<pair<bool, int>(int, int, int)> play = [&](int remaining, int current, int other) -> pair<bool, int> {
        if (!(remaining & (1 << current))) return {false, 0};
        unsigned long long key = (1ULL * remaining << 10) | (current << 5) | other;
        auto found = memo.find(key); if (found != memo.end()) return found->second;
        int fastest_win = 1000000, longest_loss = 0;
        for (int target : neighbors[current]) if (remaining & (1 << target)) {
            auto [other_wins, turns] = play(remaining ^ (1 << current), other, target);
            if (other_wins) longest_loss = max(longest_loss, turns + 1);
            else fastest_win = min(fastest_win, turns + 1);
        }
        return memo[key] = fastest_win != 1000000 ? make_pair(true, fastest_win) : make_pair(false, longest_loss);
    };
    return play(mask, aloc[0] * m + aloc[1], bloc[0] * m + bloc[1]).second;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> board, vector<int> aloc, vector<int> bloc) {  // 이기는 수는 빠르게, 지는 수는 늦게 끝내기
// int n = (int)board.size(), m = (int)board[0].size(), mask = 0;  // 격자 크기와 남은 발판 집합 구하기
// vector<vector<int>> neighbors(n * m); int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};  // 각 위치의 이동 가능 방향 선언
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) {  // 발판과 인접 칸 등록
// int pos = r * m + c; if (board[r][c]) mask |= 1 << pos;  // 발판이 있는 칸의 비트를 켜기
// for (int d = 0; d < 4; ++d) { int nr = r + dr[d], nc = c + dc[d]; if (nr >= 0 && nr < n && nc >= 0 && nc < m) neighbors[pos].push_back(nr * m + nc); }  // 격자 안의 이웃 저장
// }  // 블록 끝
// unordered_map<unsigned long long, pair<bool, int>> memo;  // 게임 상태별 승리 여부와 최적 남은 턴 수를 기억
// function<pair<bool, int>(int, int, int)> play = [&](int remaining, int current, int other) -> pair<bool, int> {  // 이번 플레이어와 상대 위치를 번갈아 바꾸며 탐색
// if (!(remaining & (1 << current))) return {false, 0};  // 현재 발판이 사라졌으면 즉시 패배
// unsigned long long key = (1ULL * remaining << 10) | (current << 5) | other;  // 최대 25칸의 상태를 하나의 키로 묶기
// auto found = memo.find(key); if (found != memo.end()) return found->second;  // 계산한 게임 상태는 재사용
// int fastest_win = 1000000, longest_loss = 0;  // 이기는 최소 턴과 지는 최대 턴 초기화
// for (int target : neighbors[current]) if (remaining & (1 << target)) {  // 남아 있는 이웃 발판으로 이동
// auto [other_wins, turns] = play(remaining ^ (1 << current), other, target);  // 현재 발판을 없애고 상대 차례의 결과 구하기
// if (other_wins) longest_loss = max(longest_loss, turns + 1);  // 패배를 피할 수 없으면 오래 버티는 선택 고르기
// else fastest_win = min(fastest_win, turns + 1);  // 이길 수 있으면 가장 빨리 끝내는 선택 고르기
// }  // 블록 끝
// return memo[key] = fastest_win != 1000000 ? make_pair(true, fastest_win) : make_pair(false, longest_loss);  // 승리 선택이 있는지에 따라 상태 결과 저장
// };  // 블록 끝
// return play(mask, aloc[0] * m + aloc[1], bloc[0] * m + bloc[1]).second;  // 최적 플레이의 전체 이동 수 반환
// }  // 블록 끝

// 풀이 요약
// 남은 발판과 두 플레이어 위치를 상태로 최적 게임을 재귀 탐색하며 이길 때는 가장 빨리, 질 때는 가장 늦게 끝나는 수 고르기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:28
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/032_92345_%EC%82%AC%EB%9D%BC%EC%A7%80%EB%8A%94_%EB%B0%9C%ED%8C%90/README.md)
