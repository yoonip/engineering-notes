# 삼각 달팽이

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68645) · Level 2 · C++

## 풀이

아래, 오른쪽, 왼쪽 위 방향으로 변의 길이를 하나씩 줄이며 삼각형을 채우고 행 순서로 펼치기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int n) {
    vector<vector<int>> board(n);
    for (int r = 0; r < n; ++r) board[r].resize(r + 1);
    int r = -1, c = 0, value = 1;
    int dr[3] = {1, 0, -1}, dc[3] = {0, 1, -1};
    for (int side = 0; side < n; ++side) {
        for (int step = 0; step < n - side; ++step) {
            r += dr[side % 3]; c += dc[side % 3];
            board[r][c] = value++;
        }
    }
    vector<int> answer;
    for (const auto& row : board) answer.insert(answer.end(), row.begin(), row.end());
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n) {  // 아래·오른쪽·대각선 위 순서로 삼각형 채우기
// vector<vector<int>> board(n);  // 행마다 길이가 다른 삼각형 저장 공간 만들기
// for (int r = 0; r < n; ++r) board[r].resize(r + 1);  // r번째 행에 r+1개의 칸 두기
// int r = -1, c = 0, value = 1;  // 첫 이동 전 위치와 채울 정수 초기화
// int dr[3] = {1, 0, -1}, dc[3] = {0, 1, -1};  // 아래, 오른쪽, 왼쪽 위의 세 방향 선언
// for (int side = 0; side < n; ++side) {  // 변을 하나 채울 때마다 방향 바꾸기
// for (int step = 0; step < n - side; ++step) {  // 남은 변의 길이만큼 이동
// r += dr[side % 3]; c += dc[side % 3];  // 현재 방향으로 한 칸 이동
// board[r][c] = value++;  // 순서대로 값을 넣고 다음 수를 준비
// }  // 블록 끝
// }  // 블록 끝
// vector<int> answer;  // 삼각형을 행 순서로 펼칠 결과 만들기
// for (const auto& row : board) answer.insert(answer.end(), row.begin(), row.end());  // 각 행을 결과 배열 뒤에 연결
// return answer;  // 펼친 삼각 달팽이 수열 반환
// }  // 블록 끝

// 풀이 요약
// 아래, 오른쪽, 왼쪽 위 방향으로 변의 길이를 하나씩 줄이며 삼각형을 채우고 행 순서로 펼치기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/061_68645_%EC%82%BC%EA%B0%81_%EB%8B%AC%ED%8C%BD%EC%9D%B4/README.md)
