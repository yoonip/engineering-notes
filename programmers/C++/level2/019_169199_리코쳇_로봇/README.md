# 리코쳇 로봇

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/169199) · Level 2 · C++

## 풀이

벽이나 경계 직전까지 미끄러진 정지 위치를 하나의 이동으로 보고 너비 우선 탐색으로 최소 횟수 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<string> board) {
    int rows = (int)board.size(), cols = (int)board[0].size();
    vector<vector<int>> distance(rows, vector<int>(cols, -1));
    queue<pair<int, int>> q;
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (board[r][c] == 'R') { distance[r][c] = 0; q.push({r, c}); }
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        if (board[r][c] == 'G') return distance[r][c];
        for (int d = 0; d < 4; ++d) {
            int nr = r, nc = c;
            while (nr + dr[d] >= 0 && nr + dr[d] < rows && nc + dc[d] >= 0 && nc + dc[d] < cols && board[nr + dr[d]][nc + dc[d]] != 'D') { nr += dr[d]; nc += dc[d]; }
            if (distance[nr][nc] == -1) {
                distance[nr][nc] = distance[r][c] + 1;
                q.push({nr, nc});
            }
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> board) {  // 미끄러진 정지 위치를 상태로 최소 이동 찾기
// int rows = (int)board.size(), cols = (int)board[0].size();  // 보드의 크기 구하기
// vector<vector<int>> distance(rows, vector<int>(cols, -1));  // 아직 도달하지 않은 위치의 이동 횟수를 -1로 두기
// queue<pair<int, int>> q;  // 너비 우선 탐색 큐 선언
// for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) if (board[r][c] == 'R') { distance[r][c] = 0; q.push({r, c}); }  // 시작 위치의 거리를 0으로 기록해 큐에 넣기
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 미끄러질 수 있는 네 방향 선언
// while (!q.empty()) {  // 이동 횟수가 적은 위치부터 처리
// auto [r, c] = q.front(); q.pop();  // 현재 위치를 큐에서 꺼내기
// if (board[r][c] == 'G') return distance[r][c];  // 목표에 처음 도착하면 최소 횟수 반환
// for (int d = 0; d < 4; ++d) {  // 네 방향의 정지 위치 찾기
// int nr = r, nc = c;  // 현재 위치에서 미끄러지기를 시작
// while (nr + dr[d] >= 0 && nr + dr[d] < rows && nc + dc[d] >= 0 && nc + dc[d] < cols && board[nr + dr[d]][nc + dc[d]] != 'D') { nr += dr[d]; nc += dc[d]; }  // 벽이나 경계 직전까지 이동
// if (distance[nr][nc] == -1) {  // 아직 도달하지 않은 정지 위치만 처리
// distance[nr][nc] = distance[r][c] + 1;  // 미끄러진 한 번을 이동 횟수에 더하기
// q.push({nr, nc});  // 다음 탐색 위치를 큐에 넣기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// return -1;  // 목표에서 멈출 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 벽이나 경계 직전까지 미끄러진 정지 위치를 하나의 이동으로 보고 너비 우선 탐색으로 최소 횟수 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/019_169199_%EB%A6%AC%EC%BD%94%EC%B3%87_%EB%A1%9C%EB%B4%87/README.md)
