# 미로 탈출

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/159993) · Level 2 · C++

## 풀이

시작점에서 레버까지, 레버에서 출구까지의 최단 거리를 각각 너비 우선 탐색으로 구해 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<string> maps) {
    int rows = (int)maps.size(), cols = (int)maps[0].size();
    pair<int, int> start, lever, exit;
    for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {
        if (maps[r][c] == 'S') start = {r, c};
        if (maps[r][c] == 'L') lever = {r, c};
        if (maps[r][c] == 'E') exit = {r, c};
    }
    auto bfs = [&](pair<int, int> source, pair<int, int> goal) {
        vector<vector<int>> distance(rows, vector<int>(cols, -1));
        queue<pair<int, int>> q;
        distance[source.first][source.second] = 0; q.push(source);
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        while (!q.empty()) {
            auto [r, c] = q.front(); q.pop();
            if (make_pair(r, c) == goal) return distance[r][c];
            for (int d = 0; d < 4; ++d) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || maps[nr][nc] == 'X' || distance[nr][nc] != -1) continue;
                distance[nr][nc] = distance[r][c] + 1;
                q.push({nr, nc});
            }
        }
        return -1;
    };
    int first = bfs(start, lever), second = bfs(lever, exit);
    return first >= 0 && second >= 0 ? first + second : -1;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> maps) {  // 시작→레버와 레버→출구의 최단 거리 합
// int rows = (int)maps.size(), cols = (int)maps[0].size();  // 미로의 행과 열 크기 구하기
// pair<int, int> start, lever, exit;  // 시작, 레버, 출구의 좌표 저장
// for (int r = 0; r < rows; ++r) for (int c = 0; c < cols; ++c) {  // 모든 칸에서 특수 위치 찾기
// if (maps[r][c] == 'S') start = {r, c};  // 시작 좌표 기록
// if (maps[r][c] == 'L') lever = {r, c};  // 레버 좌표 기록
// if (maps[r][c] == 'E') exit = {r, c};  // 출구 좌표 기록
// }  // 블록 끝
// auto bfs = [&](pair<int, int> source, pair<int, int> goal) {  // 두 좌표 사이의 최단 거리를 구하는 람다
// vector<vector<int>> distance(rows, vector<int>(cols, -1));  // 방문하지 않은 칸의 거리를 -1로 두기
// queue<pair<int, int>> q;  // 너비 우선 탐색 큐 선언
// distance[source.first][source.second] = 0; q.push(source);  // 출발점의 거리를 0으로 기록
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 상하좌우 이동량 선언
// while (!q.empty()) {  // 가까운 칸부터 차례대로 처리
// auto [r, c] = q.front(); q.pop();  // 현재 칸을 큐에서 꺼내기
// if (make_pair(r, c) == goal) return distance[r][c];  // 목표에 처음 도착하면 최소 거리 반환
// for (int d = 0; d < 4; ++d) {  // 네 방향의 이동 검사
// int nr = r + dr[d], nc = c + dc[d];  // 이웃 좌표 계산
// if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || maps[nr][nc] == 'X' || distance[nr][nc] != -1) continue;  // 범위 밖, 벽, 방문한 칸을 제외
// distance[nr][nc] = distance[r][c] + 1;  // 이동 한 칸을 거리에 더하기
// q.push({nr, nc});  // 이웃 칸을 큐에 넣기
// }  // 블록 끝
// }  // 블록 끝
// return -1;  // 도달할 수 없으면 -1 반환
// };  // 블록 끝
// int first = bfs(start, lever), second = bfs(lever, exit);  // 레버까지와 레버에서 출구까지의 거리를 각각 구하기
// return first >= 0 && second >= 0 ? first + second : -1;  // 두 구간이 모두 가능하면 거리를 더하기
// }  // 블록 끝

// 풀이 요약
// 시작점에서 레버까지, 레버에서 출구까지의 최단 거리를 각각 너비 우선 탐색으로 구해 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/022_159993_%EB%AF%B8%EB%A1%9C_%ED%83%88%EC%B6%9C/README.md)
