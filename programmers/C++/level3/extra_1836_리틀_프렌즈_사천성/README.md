# 리틀 프렌즈 사천성

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1836) · Level 3 · C++

## 풀이

사전순으로 각 문자 쌍의 한 번 이하로 꺾는 두 연결 경로를 확인하고 제거 가능한 가장 작은 문자부터 지우기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <map>
#include <string>
#include <utility>
#include <vector>
using namespace std;

string solution(int m, int n, vector<string> board) {
    map<char,vector<pair<int,int>>> positions;
    for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) if (board[r][c] >= 'A' && board[r][c] <= 'Z') positions[board[r][c]].push_back({r,c});
    auto clear = [&](int r1,int c1,int r2,int c2,char letter) {
        for (int r = min(r1,r2); r <= max(r1,r2); ++r) for (int c = min(c1,c2); c <= max(c1,c2); ++c) if (board[r][c] != '.' && board[r][c] != letter) return false;
        return true;
    };
    string answer;
    while (!positions.empty()) {
        bool removed = false;
        for (auto it = positions.begin(); it != positions.end(); ++it) {
            char letter = it->first; auto [r1,c1] = it->second[0]; auto [r2,c2] = it->second[1];
            bool first = clear(r1,c1,r1,c2,letter) && clear(r1,c2,r2,c2,letter), second = clear(r1,c1,r2,c1,letter) && clear(r2,c1,r2,c2,letter);
            if (first || second) { board[r1][c1] = board[r2][c2] = '.'; answer += letter; positions.erase(it); removed = true; break; }
        }
        if (!removed) return "IMPOSSIBLE";
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <map>  // 키를 정렬해 보관하는 map
// #include <string>  // 문자열을 담는 string
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// string solution(int m, int n, vector<string> board) {  // 연결 가능한 가장 작은 문자 쌍부터 제거
// map<char,vector<pair<int,int>>> positions;  // 문자 타일의 두 위치를 사전순으로 저장
// for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) if (board[r][c] >= 'A' && board[r][c] <= 'Z') positions[board[r][c]].push_back({r,c});  // 알파벳 타일만 등록
// auto clear = [&](int r1,int c1,int r2,int c2,char letter) {  // 직선 구간이 비어 있거나 같은 타일인지 검사
// for (int r = min(r1,r2); r <= max(r1,r2); ++r) for (int c = min(c1,c2); c <= max(c1,c2); ++c) if (board[r][c] != '.' && board[r][c] != letter) return false;  // 경로를 막는 벽이나 다른 문자가 있으면 실패
// return true;  // 구간을 통과할 수 있으면 참
// };  // 블록 끝
// string answer;  // 제거한 문자 순서 저장
// while (!positions.empty()) {  // 남은 타일을 사전순으로 하나씩 제거
// bool removed = false;  // 이번 반복에서 제거할 수 있는 쌍을 찾았는지 표시
// for (auto it = positions.begin(); it != positions.end(); ++it) {  // 현재 가능한 문자 중 가장 작은 것부터 확인
// char letter = it->first; auto [r1,c1] = it->second[0]; auto [r2,c2] = it->second[1];  // 두 타일의 좌표 읽기
// bool first = clear(r1,c1,r1,c2,letter) && clear(r1,c2,r2,c2,letter), second = clear(r1,c1,r2,c1,letter) && clear(r2,c1,r2,c2,letter);  // 한 번 이하로 꺾는 두 경로 검사
// if (first || second) { board[r1][c1] = board[r2][c2] = '.'; answer += letter; positions.erase(it); removed = true; break; }  // 연결되는 쌍을 제거하고 작은 문자부터 다시 검사
// }  // 블록 끝
// if (!removed) return "IMPOSSIBLE";  // 어떤 쌍도 제거할 수 없으면 실패
// }  // 블록 끝
// return answer;  // 사전순으로 가장 빠른 전체 제거 순서 반환
// }  // 블록 끝

// 풀이 요약
// 사전순으로 각 문자 쌍의 한 번 이하로 꺾는 두 연결 경로를 확인하고 제거 가능한 가장 작은 문자부터 지우기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/extra_1836_%EB%A6%AC%ED%8B%80_%ED%94%84%EB%A0%8C%EC%A6%88_%EC%82%AC%EC%B2%9C%EC%84%B1/README.md)
