# 자물쇠와 열쇠

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/60059) · Level 3 · C++

## 풀이

열쇠를 네 방향으로 돌리고 모든 겹치는 위치에서 자물쇠 안의 돌기 집합이 홈 집합과 정확히 같은지 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <set>
#include <utility>
#include <vector>
using namespace std;

bool solution(vector<vector<int>> key, vector<vector<int>> lock) {
    int m = (int)key.size(), n = (int)lock.size(); set<pair<int,int>> holes;
    for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) if (lock[r][c] == 0) holes.insert({r,c});
    if (holes.empty()) return true;
    vector<pair<int,int>> points; for (int r = 0; r < m; ++r) for (int c = 0; c < m; ++c) if (key[r][c] == 1) points.push_back({r,c});
    for (int turn = 0; turn < 4; ++turn) {
        for (int dr = 1 - m; dr < n; ++dr) for (int dc = 1 - m; dc < n; ++dc) {
            set<pair<int,int>> inside;
            for (auto [r,c] : points) if (r + dr >= 0 && r + dr < n && c + dc >= 0 && c + dc < n) inside.insert({r + dr,c + dc});
            if (inside == holes) return true;
        }
        for (auto& point : points) point = {point.second, m - 1 - point.first};
    }
    return false;
}

// 전체 코드 줄별 설명
// #include <set>  // 정렬된 집합과 중복을 허용하는 multiset
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// bool solution(vector<vector<int>> key, vector<vector<int>> lock) {  // 열쇠 회전·평행 이동으로 자물쇠의 홈 채우기
// int m = (int)key.size(), n = (int)lock.size(); set<pair<int,int>> holes;  // 두 격자 크기와 자물쇠의 홈 위치 저장
// for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) if (lock[r][c] == 0) holes.insert({r,c});  // 홈 칸을 모두 모으기
// if (holes.empty()) return true;  // 홈이 없으면 열쇠를 겹치지 않게 두어 열 수 있음
// vector<pair<int,int>> points; for (int r = 0; r < m; ++r) for (int c = 0; c < m; ++c) if (key[r][c] == 1) points.push_back({r,c});  // 열쇠의 돌기 좌표만 모으기
// for (int turn = 0; turn < 4; ++turn) {  // 네 회전 방향 검사
// for (int dr = 1 - m; dr < n; ++dr) for (int dc = 1 - m; dc < n; ++dc) {  // 자물쇠와 겹칠 수 있는 모든 평행 이동 검사
// set<pair<int,int>> inside;  // 현재 열쇠의 돌기 중 자물쇠 안에 있는 위치 저장
// for (auto [r,c] : points) if (r + dr >= 0 && r + dr < n && c + dc >= 0 && c + dc < n) inside.insert({r + dr,c + dc});  // 범위 안으로 들어온 돌기만 기록
// if (inside == holes) return true;  // 돌기 위치가 모든 홈과 정확히 같으면 열림
// }  // 블록 끝
// for (auto& point : points) point = {point.second, m - 1 - point.first};  // 열쇠를 90도 회전
// }  // 블록 끝
// return false;  // 맞는 회전과 위치가 없으면 거짓 반환
// }  // 블록 끝

// 풀이 요약
// 열쇠를 네 방향으로 돌리고 모든 겹치는 위치에서 자물쇠 안의 돌기 집합이 홈 집합과 정확히 같은지 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/055_60059_%EC%9E%90%EB%AC%BC%EC%87%A0%EC%99%80_%EC%97%B4%EC%87%A0/README.md)
