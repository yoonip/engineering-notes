# 블록 게임

[레벨 4 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42894) · Level 4 · C++

## 풀이

블록별 외접 직사각형에서 빈자리 두 곳을 찾음. 두 칸 모두 위에서 검은 블록을 떨어뜨릴 수 있으면 제거하고, 추가 제거가 없을 때까지 반복.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <tuple>
#include <utility>
#include <climits>
#include <cstdlib>
using namespace std;

int solution(vector<vector<int>> board) {
    int n = (int)board.size(); map<int, vector<pair<int, int>>> blocks, holes;
    for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) if (board[r][c]) blocks[board[r][c]].push_back({r, c});
    for (const auto& [number, cells] : blocks) {
        int top = n, bottom = 0, left = n, right = 0;
        for (auto [r, c] : cells) { top = min(top, r); bottom = max(bottom, r); left = min(left, c); right = max(right, c); }
        for (int r = top; r <= bottom; ++r) for (int c = left; c <= right; ++c) if (board[r][c] != number) holes[number].push_back({r, c});
    }
    int answer = 0;
    while (true) {
        vector<int> removed;
        for (const auto& [number, cells] : blocks) {
            if (holes[number].size() != 2) continue; bool possible = true;
            for (auto [r, c] : holes[number]) for (int up = 0; up <= r; ++up) if (board[up][c]) possible = false;
            if (possible) { for (auto [r, c] : cells) board[r][c] = 0; removed.push_back(number); }
        }
        if (removed.empty()) break;
        answer += removed.size(); for (int number : removed) blocks.erase(number);
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <array>  // 고정 크기 배열 array 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <map>  // 키 순서가 유지되는 맵 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <deque>  // 양 끝 삽입·삭제를 지원하는 덱 사용 준비
// #include <tuple>  // 여러 상태 값을 묶는 tuple 사용 준비
// #include <utility>  // pair·move 등 유틸리티 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(vector<vector<int>> board) {  // 블록 게임 풀이 함수 정의
//     int n = (int)board.size(); map<int, vector<pair<int, int>>> blocks, holes;  // 보드 크기와 블록별 원래 칸·채울 칸 목록 준비
//     for (int r = 0; r < n; ++r) for (int c = 0; c < n; ++c) if (board[r][c]) blocks[board[r][c]].push_back({r, c});  // 숫자가 있는 칸을 해당 블록 번호별로 수집
//     for (const auto& [number, cells] : blocks) {  // 블록별 외접 직사각형 계산
//         int top = n, bottom = 0, left = n, right = 0;  // 위·아래·왼쪽·오른쪽 경곗값 초기화
//         for (auto [r, c] : cells) { top = min(top, r); bottom = max(bottom, r); left = min(left, c); right = max(right, c); }  // 블록의 네 칸으로 외접 직사각형 경계 갱신
//         for (int r = top; r <= bottom; ++r) for (int c = left; c <= right; ++c) if (board[r][c] != number) holes[number].push_back({r, c});  // 직사각형 내부에서 현재 블록이 차지하지 않는 칸을 holes에 기록
//     }  // 블록 끝
//     int answer = 0;  // 제거한 블록 수 answer를 0으로 시작
//     while (true) {  // 새로 제거할 블록이 있는 동안 반복
//         vector<int> removed;  // 이번 순회에서 제거한 번호를 모을 배열 준비
//         for (const auto& [number, cells] : blocks) {  // 현재 남아 있는 블록을 하나씩 검사
//             if (holes[number].size() != 2) continue; bool possible = true;  // 채울 칸이 정확히 두 개가 아니면 제외하고, 나머지는 제거 가능하다고 가정
//             for (auto [r, c] : holes[number]) for (int up = 0; up <= r; ++up) if (board[up][c]) possible = false;  // 각 빈자리의 위쪽 전체 열에 다른 블록이 있는지 확인
//             if (possible) { for (auto [r, c] : cells) board[r][c] = 0; removed.push_back(number); }  // 두 자리 모두 위에서 접근 가능하면 블록 칸을 비우고 제거 번호 기록
//         }  // 블록 끝
//         if (removed.empty()) break;  // 이번 순회에 제거한 블록이 없으면 연쇄 제거 종료
//         answer += removed.size(); for (int number : removed) blocks.erase(number);  // 제거 수를 합산하고 해당 번호를 남은 블록 목록에서 삭제
//     }  // 블록 끝
//     return answer;  // 최종 제거한 블록 수 반환
// }  // 함수 끝
//

// 풀이 요약
// 블록별 외접 직사각형에서 빈자리 두 곳을 찾음. 두 칸 모두 위에서 검은 블록을 떨어뜨릴 수 있으면 제거하고, 추가 제거가 없을 때까지 반복.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_42894_%EB%B8%94%EB%A1%9D_%EA%B2%8C%EC%9E%84/README.md)
