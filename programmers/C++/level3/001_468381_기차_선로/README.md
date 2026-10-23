# 기차 선로

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468381) · Level 3 · C++

## 풀이

필수 선로와 교차 선로의 두 축 통과를 비트 마스크로 관리하고 가능한 선로 배치를 되돌리며 시작부터 도착까지의 경로 수 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <array>
#include <functional>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<vector<int>> grid) {
    int n = (int)grid.size(), m = (int)grid[0].size(), size = n * m;
    vector<int> original, rails;
    for (const auto& row : grid) original.insert(original.end(), row.begin(), row.end());
    rails = original;
    vector<array<int, 4>> neighbors(size); int required = 0;
    for (int pos = 0; pos < size; ++pos) {
        int r = pos / m, c = pos % m;
        neighbors[pos] = {c + 1 < m ? pos + 1 : -1, r + 1 < n ? pos + m : -1, c ? pos - 1 : -1, r ? pos - m : -1};
        if (original[pos] > 0) required |= 1 << pos;
    }
    int ends[8] = {0, 5, 10, 15, 12, 9, 3, 6};
    vector<vector<pair<int, int>>> choices(4);
    for (int direction = 0; direction < 4; ++direction) for (int kind : {1, 2, 4, 5, 6, 7}) {
        int entry = (direction + 2) % 4;
        if (ends[kind] & (1 << entry)) {
            int exit_bit = ends[kind] ^ (1 << entry);
            int exit_direction = 0; while ((1 << exit_direction) != exit_bit) ++exit_direction;
            choices[direction].push_back({kind, exit_direction});
        }
    }
    vector<int> visited(size, 0); visited[0] = 1;
    function<int(int, int, int, int)> dfs = [&](int pos, int direction, int remaining, int pending) {
        if (pos < 0 || original[pos] == -1) return 0;
        int axis = 1 << (direction % 2), kind = rails[pos], used = visited[pos];
        if (used) {
            if ((used & axis) || (kind != 1 && kind != 2 && kind != 3)) return 0;
            if (kind != 3 && original[pos] != 0) return 0;
            rails[pos] = 3; visited[pos] = 3;
            int result = dfs(neighbors[pos][direction], direction, remaining, pending & ~(1 << pos));
            rails[pos] = kind; visited[pos] = used;
            return result;
        }
        remaining &= ~(1 << pos);
        if (pos == size - 1) {
            bool entry = (kind == 1 && direction == 0) || (kind == 2 && direction == 1);
            return int(entry && remaining == 0 && pending == 0);
        }
        visited[pos] = axis; int result = 0;
        if (kind == 3) result = dfs(neighbors[pos][direction], direction, remaining, pending | (1 << pos));
        else for (auto [candidate, exit_direction] : choices[direction]) {
            if (kind != 0 && kind != candidate) continue;
            rails[pos] = candidate; visited[pos] = candidate <= 2 ? axis : 3;
            result += dfs(neighbors[pos][exit_direction], exit_direction, remaining, pending);
        }
        rails[pos] = kind; visited[pos] = 0;
        return result;
    };
    return dfs(1, 0, required & ~1, 0);
}

// 전체 코드 줄별 설명
// #include <array>  // 크기가 고정된 array
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> grid) {  // 필수 선로를 모두 통과하는 유효한 배치 수 찾기
// int n = (int)grid.size(), m = (int)grid[0].size(), size = n * m;  // 격자 크기와 전체 칸 수 구하기
// vector<int> original, rails;  // 원래 선로와 탐색 중 배치한 선로를 따로 저장
// for (const auto& row : grid) original.insert(original.end(), row.begin(), row.end());  // 격자를 일차원 위치로 펼치기
// rails = original;  // 탐색할 선로 배치를 원본으로 초기화
// vector<array<int, 4>> neighbors(size); int required = 0;  // 네 방향 이웃과 반드시 지나야 할 칸의 비트 마스크 만들기
// for (int pos = 0; pos < size; ++pos) {  // 각 위치의 이웃과 필수 여부 계산
// int r = pos / m, c = pos % m;  // 일차원 위치를 행과 열로 바꾸기
// neighbors[pos] = {c + 1 < m ? pos + 1 : -1, r + 1 < n ? pos + m : -1, c ? pos - 1 : -1, r ? pos - m : -1};  // 오른쪽, 아래, 왼쪽, 위의 이웃 기록
// if (original[pos] > 0) required |= 1 << pos;  // 고정된 선로 칸을 필수 방문 마스크에 넣기
// }  // 블록 끝
// int ends[8] = {0, 5, 10, 15, 12, 9, 3, 6};  // 각 선로가 연결하는 방향을 네 비트로 표현
// vector<vector<pair<int, int>>> choices(4);  // 진입 방향별로 가능한 선로 종류와 출구 방향 저장
// for (int direction = 0; direction < 4; ++direction) for (int kind : {1, 2, 4, 5, 6, 7}) {  // 교차 선로를 제외한 단일 통과 배치 구하기
// int entry = (direction + 2) % 4;  // 이동 방향의 반대가 현재 칸의 진입 연결점
// if (ends[kind] & (1 << entry)) {  // 선로가 현재 진입점을 연결하는지 검사
// int exit_bit = ends[kind] ^ (1 << entry);  // 남은 하나의 연결점을 출구로 구하기
// int exit_direction = 0; while ((1 << exit_direction) != exit_bit) ++exit_direction;  // 출구 비트를 방향 인덱스로 바꾸기
// choices[direction].push_back({kind, exit_direction});  // 가능한 선로 배치 저장
// }  // 블록 끝
// }  // 블록 끝
// vector<int> visited(size, 0); visited[0] = 1;  // 첫 칸의 가로 통과를 초기 방문 상태로 두기
// function<int(int, int, int, int)> dfs = [&](int pos, int direction, int remaining, int pending) {  // 위치와 방향 및 미완료 필수 통과를 상태로 탐색
// if (pos < 0 || original[pos] == -1) return 0;  // 격자 밖이나 막힌 칸으로 가면 실패
// int axis = 1 << (direction % 2), kind = rails[pos], used = visited[pos];  // 현재 통과 축, 선로 종류, 기존 방문 축 읽기
// if (used) {  // 이미 지나간 칸을 다른 축으로 다시 통과할 수 있는지 검사
// if ((used & axis) || (kind != 1 && kind != 2 && kind != 3)) return 0;  // 같은 축 재방문이나 곡선의 재방문은 제외
// if (kind != 3 && original[pos] != 0) return 0;  // 고정된 직선은 교차 선로로 바꿀 수 없음
// rails[pos] = 3; visited[pos] = 3;  // 빈 칸의 직선을 교차로 완성하고 두 축을 방문 처리
// int result = dfs(neighbors[pos][direction], direction, remaining, pending & ~(1 << pos));  // 직진하며 교차 선로의 남은 축 요구 제거
// rails[pos] = kind; visited[pos] = used;  // 다른 경로를 위해 기존 배치를 복구하기
// return result;  // 현재 재방문으로 가능한 완성 수 반환
// }  // 블록 끝
// remaining &= ~(1 << pos);  // 처음 방문한 필수 칸을 남은 마스크에서 제거
// if (pos == size - 1) {  // 도착 칸에서 모든 조건 확인
// bool entry = (kind == 1 && direction == 0) || (kind == 2 && direction == 1);  // 도착 선로의 진입 방향이 맞는지 검사
// return int(entry && remaining == 0 && pending == 0);  // 모든 필수 선로와 교차 축을 통과했을 때만 세기
// }  // 블록 끝
// visited[pos] = axis; int result = 0;  // 현재 통과 축을 기록하고 분기 결과 초기화
// if (kind == 3) result = dfs(neighbors[pos][direction], direction, remaining, pending | (1 << pos));  // 고정 교차 선로는 직진하고 다른 축 통과를 요구하기
// else for (auto [candidate, exit_direction] : choices[direction]) {  // 진입 가능한 단일 선로 배치를 모두 선택
// if (kind != 0 && kind != candidate) continue;  // 고정 선로와 다른 배치는 제외
// rails[pos] = candidate; visited[pos] = candidate <= 2 ? axis : 3;  // 직선은 현재 축만, 곡선은 재방문 불가로 표시
// result += dfs(neighbors[pos][exit_direction], exit_direction, remaining, pending);  // 출구 방향으로 이어지는 경로 수를 더하기
// }  // 블록 끝
// rails[pos] = kind; visited[pos] = 0;  // 배치와 방문 상태 되돌리기
// return result;  // 현재 칸에서 가능한 완성 수 반환
// };  // 블록 끝
// return dfs(1, 0, required & ~1, 0);  // 시작 칸 오른쪽에서 가로 방향으로 탐색을 시작
// }  // 블록 끝

// 풀이 요약
// 필수 선로와 교차 선로의 두 축 통과를 비트 마스크로 관리하고 가능한 선로 배치를 되돌리며 시작부터 도착까지의 경로 수 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:41:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/001_468381_%EA%B8%B0%EC%B0%A8_%EC%84%A0%EB%A1%9C/README.md)
