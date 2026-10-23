# 지게차와 크레인

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/388353) · Level 2 · C++

## 풀이

바깥 테두리에서 연결된 빈 공간을 탐색해 지게차가 닿는 컨테이너를 찾고, 크레인 요청은 같은 종류 전체 제거

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<string> storage, vector<string> requests) {
    int n = (int)storage.size(), m = (int)storage[0].size();
    vector<string> board(n + 2, string(m + 2, '.'));
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) board[r + 1][c + 1] = storage[r][c];
    int remaining = n * m;
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (const string& request : requests) {
        char target = request[0];
        vector<pair<int, int>> removed;
        if (request.size() == 2) {
            for (int r = 1; r <= n; ++r) for (int c = 1; c <= m; ++c) if (board[r][c] == target) removed.push_back({r, c});
        } else {
            vector<vector<bool>> visited(n + 2, vector<bool>(m + 2, false));
            queue<pair<int, int>> q;
            q.push({0, 0}); visited[0][0] = true;
            while (!q.empty()) {
                auto [r, c] = q.front(); q.pop();
                for (int d = 0; d < 4; ++d) {
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nr >= n + 2 || nc < 0 || nc >= m + 2 || visited[nr][nc]) continue;
                    visited[nr][nc] = true;
                    if (board[nr][nc] == '.') q.push({nr, nc});
                    else if (board[nr][nc] == target) removed.push_back({nr, nc});
                }
            }
        }
        for (auto [r, c] : removed) board[r][c] = '.';
        remaining -= (int)removed.size();
    }
    return remaining;
}

// 전체 코드 줄별 설명
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> storage, vector<string> requests) {  // 지게차의 외부 접근과 크레인의 전체 제거 구분
// int n = (int)storage.size(), m = (int)storage[0].size();  // 창고의 행과 열 수 구하기
// vector<string> board(n + 2, string(m + 2, '.'));  // 창고 바깥을 한 칸의 빈 공간으로 둘러싸기
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) board[r + 1][c + 1] = storage[r][c];  // 원래 컨테이너를 테두리 안쪽으로 복사
// int remaining = n * m;  // 남은 컨테이너 수 초기화
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 상하좌우 이동량 선언
// for (const string& request : requests) {  // 요청을 입력 순서대로 처리
// char target = request[0];  // 이번에 꺼낼 컨테이너 종류 읽기
// vector<pair<int, int>> removed;  // 동시에 제거할 위치를 먼저 모으기
// if (request.size() == 2) {  // 크레인은 같은 종류의 모든 컨테이너 꺼내기
// for (int r = 1; r <= n; ++r) for (int c = 1; c <= m; ++c) if (board[r][c] == target) removed.push_back({r, c});  // 해당 종류의 모든 위치를 수집
// } else {  // 지게차는 바깥 빈 공간에 닿는 컨테이너만 꺼내기
// vector<vector<bool>> visited(n + 2, vector<bool>(m + 2, false));  // 빈 공간 탐색의 방문 표시 만들기
// queue<pair<int, int>> q;  // 너비 우선 탐색 큐 선언
// q.push({0, 0}); visited[0][0] = true;  // 바깥 테두리에서 탐색을 시작
// while (!q.empty()) {  // 바깥과 연결된 모든 빈 공간 찾기
// auto [r, c] = q.front(); q.pop();  // 큐 앞에서 현재 위치 꺼내기
// for (int d = 0; d < 4; ++d) {  // 네 방향의 이웃 검사
// int nr = r + dr[d], nc = c + dc[d];  // 이웃 좌표 계산
// if (nr < 0 || nr >= n + 2 || nc < 0 || nc >= m + 2 || visited[nr][nc]) continue;  // 범위 밖이거나 방문한 위치는 제외
// visited[nr][nc] = true;  // 같은 위치를 중복 처리하지 않도록 표시
// if (board[nr][nc] == '.') q.push({nr, nc});  // 빈 공간이면 계속 이동
// else if (board[nr][nc] == target) removed.push_back({nr, nc});  // 대상 컨테이너이면 제거 목록에 넣기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝
// for (auto [r, c] : removed) board[r][c] = '.';  // 현재 요청에서 찾은 위치를 모두 빈 공간으로 바꾸기
// remaining -= (int)removed.size();  // 제거한 수만큼 남은 컨테이너 수 줄이기
// }  // 블록 끝
// return remaining;  // 모든 요청 뒤 남은 수 반환
// }  // 블록 끝

// 풀이 요약
// 바깥 테두리에서 연결된 빈 공간을 탐색해 지게차가 닿는 컨테이너를 찾고, 크레인 요청은 같은 종류 전체 제거
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/007_388353_%EC%A7%80%EA%B2%8C%EC%B0%A8%EC%99%80_%ED%81%AC%EB%A0%88%EC%9D%B8/README.md)
