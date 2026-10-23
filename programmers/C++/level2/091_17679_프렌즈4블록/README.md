# [1차] 프렌즈4블록

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17679) · Level 2 · C++

## 풀이

같은 문자로 이루어진 모든 2×2 묶음을 동시에 제거하고 열별로 블록을 내려 더 제거할 묶음이 없을 때까지 반복

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

int solution(int m, int n, vector<string> board) {
    int answer = 0;
    for (;;) {
        vector<vector<bool>> removed(m, vector<bool>(n, false));
        for (int r = 0; r + 1 < m; ++r) for (int c = 0; c + 1 < n; ++c) {
            char value = board[r][c];
            if (value != '.' && value == board[r + 1][c] && value == board[r][c + 1] && value == board[r + 1][c + 1]) removed[r][c] = removed[r + 1][c] = removed[r][c + 1] = removed[r + 1][c + 1] = true;
        }
        int count = 0;
        for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) if (removed[r][c]) { board[r][c] = '.'; ++count; }
        if (count == 0) return answer;
        answer += count;
        for (int c = 0; c < n; ++c) {
            int write = m - 1;
            for (int r = m - 1; r >= 0; --r) if (board[r][c] != '.') board[write--][c] = board[r][c];
            while (write >= 0) board[write--][c] = '.';
        }
    }
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int m, int n, vector<string> board) {  // 2×2 블록을 동시에 지우고 남은 블록을 아래로 모으기
// int answer = 0;  // 제거한 블록 수 초기화
// for (;;) {  // 더 제거할 묶음이 없을 때까지 반복
// vector<vector<bool>> removed(m, vector<bool>(n, false));  // 이번 단계에서 제거할 위치를 표시
// for (int r = 0; r + 1 < m; ++r) for (int c = 0; c + 1 < n; ++c) {  // 모든 2×2 시작 위치 검사
// char value = board[r][c];  // 묶음의 기준 문자 읽기
// if (value != '.' && value == board[r + 1][c] && value == board[r][c + 1] && value == board[r + 1][c + 1]) removed[r][c] = removed[r + 1][c] = removed[r][c + 1] = removed[r + 1][c + 1] = true;  // 같은 블록 네 개의 위치를 동시에 표시
// }  // 블록 끝
// int count = 0;  // 이번 단계 제거 수 초기화
// for (int r = 0; r < m; ++r) for (int c = 0; c < n; ++c) if (removed[r][c]) { board[r][c] = '.'; ++count; }  // 표시한 블록을 빈 칸으로 바꾸고 세기
// if (count == 0) return answer;  // 제거할 블록이 없으면 전체 수 반환
// answer += count;  // 이번 제거 수를 합계에 더하기
// for (int c = 0; c < n; ++c) {  // 열별로 남은 블록을 아래로 떨어뜨리기
// int write = m - 1;  // 다음 블록을 둘 가장 아래 위치
// for (int r = m - 1; r >= 0; --r) if (board[r][c] != '.') board[write--][c] = board[r][c];  // 아래부터 남은 블록 모으기
// while (write >= 0) board[write--][c] = '.';  // 위쪽의 남은 칸을 비우기
// }  // 블록 끝
// }  // 블록 끝
// }  // 블록 끝

// 풀이 요약
// 같은 문자로 이루어진 모든 2×2 묶음을 동시에 제거하고 열별로 블록을 내려 더 제거할 묶음이 없을 때까지 반복
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/091_17679_%ED%94%84%EB%A0%8C%EC%A6%884%EB%B8%94%EB%A1%9D/README.md)
