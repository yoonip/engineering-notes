# 혼자서 하는 틱택토

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/160585) · Level 2 · C++

## 풀이

말의 개수가 번갈아 두는 순서에 맞는지 검사하고 행, 열, 대각선의 승리 상태와 마지막 차례가 일치하는지 확인

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

int solution(vector<string> board) {
    int o = 0, x = 0;
    for (const string& row : board) for (char c : row) { o += c == 'O'; x += c == 'X'; }
    if (o != x && o != x + 1) return 0;
    auto wins = [&](char mark) {
        for (int i = 0; i < 3; ++i) {
            if (board[i][0] == mark && board[i][1] == mark && board[i][2] == mark) return true;
            if (board[0][i] == mark && board[1][i] == mark && board[2][i] == mark) return true;
        }
        return (board[0][0] == mark && board[1][1] == mark && board[2][2] == mark) || (board[0][2] == mark && board[1][1] == mark && board[2][0] == mark);
    };
    bool ow = wins('O'), xw = wins('X');
    if (ow && xw) return 0;
    if (ow && o != x + 1) return 0;
    if (xw && o != x) return 0;
    return 1;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<string> board) {  // 말 개수와 승리 상태가 가능한 진행인지 판정
// int o = 0, x = 0;  // 두 플레이어가 놓은 말의 수 초기화
// for (const string& row : board) for (char c : row) { o += c == 'O'; x += c == 'X'; }  // 각 칸의 문자를 비교해 O와 X의 개수 세기
// if (o != x && o != x + 1) return 0;  // O가 선공인 번갈아 두기 규칙에 맞지 않으면 제외
// auto wins = [&](char mark) {  // 지정한 말이 세 칸을 연결했는지 검사
// for (int i = 0; i < 3; ++i) {  // 세 행과 세 열 검사
// if (board[i][0] == mark && board[i][1] == mark && board[i][2] == mark) return true;  // 같은 행의 세 말이 일치하면 승리
// if (board[0][i] == mark && board[1][i] == mark && board[2][i] == mark) return true;  // 같은 열의 세 말이 일치하면 승리
// }  // 블록 끝
// return (board[0][0] == mark && board[1][1] == mark && board[2][2] == mark) || (board[0][2] == mark && board[1][1] == mark && board[2][0] == mark);  // 두 대각선의 승리 여부 반환
// };  // 블록 끝
// bool ow = wins('O'), xw = wins('X');  // 각 플레이어의 승리 여부 구하기
// if (ow && xw) return 0;  // 두 플레이어가 동시에 승리한 상태는 불가능
// if (ow && o != x + 1) return 0;  // O가 이겼다면 O가 한 번 더 두어야 함
// if (xw && o != x) return 0;  // X가 이겼다면 두 말의 수가 같아야 함
// return 1;  // 모든 조건을 만족하면 가능한 상태
// }  // 블록 끝

// 풀이 요약
// 말의 개수가 번갈아 두는 순서에 맞는지 검사하고 행, 열, 대각선의 승리 상태와 마지막 차례가 일치하는지 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/021_160585_%ED%98%BC%EC%9E%90%EC%84%9C_%ED%95%98%EB%8A%94_%ED%8B%B1%ED%83%9D%ED%86%A0/README.md)
