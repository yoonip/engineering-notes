# 안전지대

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120866) · Level 0 · C++

## 풀이

각 칸을 중심으로 자기 자신과 주변 여덟 칸을 확인. 격자 안에 있는 검사 대상 중 지뢰가 하나도 없을 때만 안전한 칸의 개수를 늘립니다

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

int solution(vector<vector<int>> board) {
    int rows = board.size(), cols = board[0].size(), answer = 0;
    for (int y = 0; y < rows; ++y)
        for (int x = 0; x < cols; ++x) {
            bool safe = true;
            for (int dy = -1; dy <= 1; ++dy)
                for (int dx = -1; dx <= 1; ++dx) {
                    int ny = y + dy, nx = x + dx;
                    if (ny >= 0 && ny < rows && nx >= 0 && nx < cols && board[ny][nx]) safe = false;
                }
            answer += safe;
        }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<vector<int>> board) {  // 안전지대 풀이 시작
//     int rows = board.size(), cols = board[0].size(), answer = 0;  // rows와 cols에 격자의 행·열 수를 저장하고, 안전한 칸을 셀 answer를 0으로 초기화
//     for (int y = 0; y < rows; ++y)  // 바깥 for로 안전 여부를 검사할 칸의 행 인덱스 y를 순회
//         for (int x = 0; x < cols; ++x) {  // 안쪽 for로 같은 행의 열 인덱스 x를 순회하여 모든 칸을 검사
//             bool safe = true;  // 현재 칸을 일단 안전하다고 표시하는 bool 변수 safe를 true로 초기화
//             for (int dy = -1; dy <= 1; ++dy)  // 행 방향 차이 dy를 -1부터 1까지 순회하여 현재 칸의 위·같은 행·아래 행을 확인
//                 for (int dx = -1; dx <= 1; ++dx) {  // 열 방향 차이 dx를 -1부터 1까지 순회하여 현재 칸을 포함한 3×3 영역의 모든 위치를 확인
//                     int ny = y + dy, nx = x + dx;  // ny와 nx에 현재 칸 (y, x)에서 (dy, dx)만큼 떨어진 이웃 좌표를 계산
//                     if (ny >= 0 && ny < rows && nx >= 0 && nx < cols && board[ny][nx]) safe = false;  // &&의 왼쪽 조건으로 이웃이 격자 안에 있는지 먼저 검사. 범위 안의 board[ny][nx]가 1이면 지뢰이므로 현재 칸의 safe를 false로 바꾸기
//                 }  // 블록 끝
//             answer += safe;  // 3×3 영역에 지뢰가 없어 safe가 true인 경우에만 answer에 1을 더하기
//         }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 칸을 중심으로 자기 자신과 주변 여덟 칸을 확인. 격자 안에 있는 검사 대상 중 지뢰가 하나도 없을 때만 안전한 칸의 개수를 늘립니다
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:30:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120866_%EC%95%88%EC%A0%84%EC%A7%80%EB%8C%80/README.md)
