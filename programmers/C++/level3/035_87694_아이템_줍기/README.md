# 아이템 줍기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/87694) · Level 3 · C++

## 풀이

좌표를 두 배로 늘려 직사각형 합집합의 외곽선만 남긴 뒤 너비 우선 탐색으로 아이템까지 거리 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <array>
#include <queue>
#include <vector>
using namespace std;

int solution(vector<vector<int>> rectangle, int characterX, int characterY, int itemX, int itemY) {
    vector<vector<int>> board(102, vector<int>(102, 0));
    for (auto& rect : rectangle) for (int& value : rect) value *= 2;
    for (const auto& rect : rectangle) for (int y = rect[1]; y <= rect[3]; ++y) for (int x = rect[0]; x <= rect[2]; ++x) board[y][x] = 1;
    for (const auto& rect : rectangle) for (int y = rect[1] + 1; y < rect[3]; ++y) for (int x = rect[0] + 1; x < rect[2]; ++x) board[y][x] = 0;
    queue<array<int, 3>> q; q.push({characterX * 2, characterY * 2, 0}); board[characterY * 2][characterX * 2] = 0;
    int dx[4] = {1,-1,0,0}, dy[4] = {0,0,1,-1};
    while (!q.empty()) {
        auto [x, y, distance] = q.front(); q.pop();
        if (x == itemX * 2 && y == itemY * 2) return distance / 2;
        for (int d = 0; d < 4; ++d) { int nx = x + dx[d], ny = y + dy[d]; if (nx >= 0 && nx < 102 && ny >= 0 && ny < 102 && board[ny][nx] == 1) { board[ny][nx] = 0; q.push({nx, ny, distance + 1}); } }
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> rectangle, int characterX, int characterY, int itemX, int itemY) {  // 두 배 좌표의 외곽선을 따라 아이템 최단 거리 찾기
// vector<vector<int>> board(102, vector<int>(102, 0));  // 좌표를 두 배로 늘린 외곽선 격자 만들기
// for (auto& rect : rectangle) for (int& value : rect) value *= 2;  // 꼭짓점이 붙은 경우를 구분하도록 모든 좌표를 두 배로 바꾸기
// for (const auto& rect : rectangle) for (int y = rect[1]; y <= rect[3]; ++y) for (int x = rect[0]; x <= rect[2]; ++x) board[y][x] = 1;  // 모든 직사각형 영역 채우기
// for (const auto& rect : rectangle) for (int y = rect[1] + 1; y < rect[3]; ++y) for (int x = rect[0] + 1; x < rect[2]; ++x) board[y][x] = 0;  // 각 직사각형의 내부를 지워 합집합 외곽선만 남기기
// queue<array<int, 3>> q; q.push({characterX * 2, characterY * 2, 0}); board[characterY * 2][characterX * 2] = 0;  // 시작점을 방문 처리해 큐에 넣기
// int dx[4] = {1,-1,0,0}, dy[4] = {0,0,1,-1};  // 네 방향 이동량 선언
// while (!q.empty()) {  // 외곽선을 따라 너비 우선 탐색
// auto [x, y, distance] = q.front(); q.pop();  // 현재 좌표와 이동 거리 꺼내기
// if (x == itemX * 2 && y == itemY * 2) return distance / 2;  // 목표에 도착하면 원래 좌표 단위로 거리를 돌려주기
// for (int d = 0; d < 4; ++d) { int nx = x + dx[d], ny = y + dy[d]; if (nx >= 0 && nx < 102 && ny >= 0 && ny < 102 && board[ny][nx] == 1) { board[ny][nx] = 0; q.push({nx, ny, distance + 1}); } }  // 아직 방문하지 않은 외곽선 칸으로 이동
// }  // 블록 끝
// return 0;  // 유효한 경로가 없을 때의 기본 반환
// }  // 블록 끝

// 풀이 요약
// 좌표를 두 배로 늘려 직사각형 합집합의 외곽선만 남긴 뒤 너비 우선 탐색으로 아이템까지 거리 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:15
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/035_87694_%EC%95%84%EC%9D%B4%ED%85%9C_%EC%A4%8D%EA%B8%B0/README.md)
