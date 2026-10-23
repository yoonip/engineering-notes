# 게임 맵 최단거리

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1844) · Level 2 · C++

## 풀이

통로를 따라 너비 우선 탐색으로 시작 칸을 포함한 최단 거리를 구하고 도달할 수 없으면 -1 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <queue>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<vector<int>> maps) {
    int rows = (int)maps.size(), cols = (int)maps[0].size();
    vector<vector<int>> distance(rows, vector<int>(cols, 0));
    queue<pair<int, int>> q; distance[0][0] = 1; q.push({0, 0});
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        if (r == rows - 1 && c == cols - 1) return distance[r][c];
        for (int d = 0; d < 4; ++d) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || !maps[nr][nc] || distance[nr][nc]) continue;
            distance[nr][nc] = distance[r][c] + 1; q.push({nr, nc});
        }
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> maps) {  // 통로만 따라 목적지까지 최소 칸 수 탐색
// int rows = (int)maps.size(), cols = (int)maps[0].size();  // 게임 맵의 크기 구하기
// vector<vector<int>> distance(rows, vector<int>(cols, 0));  // 아직 방문하지 않은 칸의 거리를 0으로 두기
// queue<pair<int, int>> q; distance[0][0] = 1; q.push({0, 0});  // 시작 칸도 포함한 거리 1로 탐색을 시작
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 상하좌우 이동량 선언
// while (!q.empty()) {  // 거리순으로 칸 탐색
// auto [r, c] = q.front(); q.pop();  // 현재 칸을 큐에서 꺼내기
// if (r == rows - 1 && c == cols - 1) return distance[r][c];  // 상대 진영에 도착하면 최단 거리 반환
// for (int d = 0; d < 4; ++d) {  // 네 방향의 이웃 검사
// int nr = r + dr[d], nc = c + dc[d];  // 다음 좌표 계산
// if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || !maps[nr][nc] || distance[nr][nc]) continue;  // 범위 밖, 벽, 방문한 칸을 제외
// distance[nr][nc] = distance[r][c] + 1; q.push({nr, nc});  // 이웃의 거리를 기록하고 큐에 넣기
// }  // 블록 끝
// }  // 블록 끝
// return -1;  // 상대 진영에 도달할 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// 통로를 따라 너비 우선 탐색으로 시작 칸을 포함한 최단 거리를 구하고 도달할 수 없으면 -1 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/extra_1844_%EA%B2%8C%EC%9E%84_%EB%A7%B5_%EC%B5%9C%EB%8B%A8%EA%B1%B0%EB%A6%AC/README.md)
