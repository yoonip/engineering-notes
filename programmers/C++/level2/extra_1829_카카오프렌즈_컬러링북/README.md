# 카카오프렌즈 컬러링북

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1829) · Level 2 · C++

## 풀이

같은 색으로 상하좌우 연결된 칸을 깊이 우선 탐색해 영역 수와 최대 영역 크기 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(int m, int n, vector<vector<int>> picture) {
    int areas = 0, largest = 0;
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) {
        int color = picture[r][c];
        if (color == 0) continue;
        ++areas; picture[r][c] = 0;
        vector<pair<int, int>> stack{{r, c}}; int size = 0;
        while (!stack.empty()) {
            auto [x, y] = stack.back(); stack.pop_back(); ++size;
            for (int d = 0; d < 4; ++d) {
                int nx = x + dr[d], ny = y + dc[d];
                if (nx >= 0 && nx < m && ny >= 0 && ny < n && picture[nx][ny] == color) { picture[nx][ny] = 0; stack.push_back({nx, ny}); }
            }
        }
        largest = max(largest, size);
    }
    return {areas, largest};
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int m, int n, vector<vector<int>> picture) {  // 같은 색 연결 영역의 개수와 최대 크기 계산
// int areas = 0, largest = 0;  // 영역 수와 최대 영역 크기 초기화
// int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};  // 같은 색을 연결할 네 방향 선언
// for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) {  // 그림의 모든 칸 검사
// int color = picture[r][c];  // 현재 칸의 색 읽기
// if (color == 0) continue;  // 빈 칸이나 이미 탐색한 칸은 건너뛰기
// ++areas; picture[r][c] = 0;  // 새 영역을 세고 시작 칸을 방문 처리
// vector<pair<int, int>> stack{{r, c}}; int size = 0;  // 영역 탐색 스택과 크기 초기화
// while (!stack.empty()) {  // 같은 색으로 연결된 칸을 모두 찾기
// auto [x, y] = stack.back(); stack.pop_back(); ++size;  // 다음 칸을 꺼내 영역 크기 늘리기
// for (int d = 0; d < 4; ++d) {  // 네 방향의 이웃 검사
// int nx = x + dr[d], ny = y + dc[d];  // 이웃 좌표 계산
// if (nx >= 0 && nx < m && ny >= 0 && ny < n && picture[nx][ny] == color) { picture[nx][ny] = 0; stack.push_back({nx, ny}); }  // 같은 색의 미방문 칸을 표시하고 탐색에 추가
// }  // 블록 끝
// }  // 블록 끝
// largest = max(largest, size);  // 가장 큰 영역 크기 갱신
// }  // 블록 끝
// return {areas, largest};  // 영역 수와 최대 영역 크기 반환
// }  // 블록 끝

// 풀이 요약
// 같은 색으로 상하좌우 연결된 칸을 깊이 우선 탐색해 영역 수와 최대 영역 크기 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_1829_%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88_%EC%BB%AC%EB%9F%AC%EB%A7%81%EB%B6%81/README.md)
