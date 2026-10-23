# 파괴되지 않은 건물

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92344) · Level 3 · C++

## 풀이

각 직사각형 변화량을 네 꼭짓점에 기록하고 가로 및 세로 누적합으로 모든 칸의 최종 내구도 계산

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(vector<vector<int>> board, vector<vector<int>> skill) {
    int n = (int)board.size(), m = (int)board[0].size();
    vector<vector<int>> difference(n + 1, vector<int>(m + 1, 0));
    for (const auto& s : skill) {
        int change = s[0] == 1 ? -s[5] : s[5];
        difference[s[1]][s[2]] += change; difference[s[1]][s[4] + 1] -= change;
        difference[s[3] + 1][s[2]] -= change; difference[s[3] + 1][s[4] + 1] += change;
    }
    for (int r = 0; r < n; ++r) for (int c = 1; c < m; ++c) difference[r][c] += difference[r][c - 1];
    for (int r = 1; r < n; ++r) for (int c = 0; c < m; ++c) difference[r][c] += difference[r - 1][c];
    int answer = 0;
    for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) answer += board[r][c] + difference[r][c] > 0;
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> board, vector<vector<int>> skill) {  // 직사각형 변화량을 누적해 살아남은 건물 세기
// int n = (int)board.size(), m = (int)board[0].size();  // 건물 격자의 크기 구하기
// vector<vector<int>> difference(n + 1, vector<int>(m + 1, 0));  // 직사각형 변화량의 네 꼭짓점 저장
// for (const auto& s : skill) {  // 공격과 회복 요청 등록
// int change = s[0] == 1 ? -s[5] : s[5];  // 공격은 음수, 회복은 양수로 바꾸기
// difference[s[1]][s[2]] += change; difference[s[1]][s[4] + 1] -= change;  // 위쪽 두 꼭짓점에 변화량 기록
// difference[s[3] + 1][s[2]] -= change; difference[s[3] + 1][s[4] + 1] += change;  // 아래쪽 두 꼭짓점에 반대 변화 기록
// }  // 블록 끝
// for (int r = 0; r < n; ++r) for (int c = 1; c < m; ++c) difference[r][c] += difference[r][c - 1];  // 가로 누적합으로 행의 변화량을 펼치기
// for (int r = 1; r < n; ++r) for (int c = 0; c < m; ++c) difference[r][c] += difference[r - 1][c];  // 세로 누적합으로 각 칸의 최종 변화량 구하기
// int answer = 0;  // 남은 건물 수 초기화
// for (int r = 0; r < n; ++r) for (int c = 0; c < m; ++c) answer += board[r][c] + difference[r][c] > 0;  // 최종 내구도가 양수인 건물 세기
// return answer;  // 파괴되지 않은 건물 수 반환
// }  // 블록 끝

// 풀이 요약
// 각 직사각형 변화량을 네 꼭짓점에 기록하고 가로 및 세로 누적합으로 모든 칸의 최종 내구도 계산
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/033_92344_%ED%8C%8C%EA%B4%B4%EB%90%98%EC%A7%80_%EC%95%8A%EC%9D%80_%EA%B1%B4%EB%AC%BC/README.md)
