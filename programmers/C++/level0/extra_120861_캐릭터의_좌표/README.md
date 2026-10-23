# 캐릭터의 좌표

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120861) · Level 0 · C++

## 풀이

이동할 후보 좌표를 먼저 만들고 지도 경계 안에 있을 때만 반영

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

vector<int> solution(vector<string> keyinput, vector<int> board) {
    vector<int> answer(2);
    for (const string& key : keyinput) {
        int x = answer[0], y = answer[1];
        if (key == "left") --x;
        else if (key == "right") ++x;
        else if (key == "up") ++y;
        else --y;
        if (abs(x) <= board[0] / 2 && abs(y) <= board[1] / 2) answer = {x, y};
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
// vector<int> solution(vector<string> keyinput, vector<int> board) {  // 캐릭터의 좌표 풀이 시작
//     vector<int> answer(2);  // 출발점 (0, 0)에서의 최종 x·y 좌표
//     for (const string& key : keyinput) {  // 입력한 방향키를 순서대로 적용
//         int x = answer[0], y = answer[1];  // 경계 검사를 위해 현재 좌표를 이동 후보로 복사
//         if (key == "left") --x;  // 왼쪽 이동 후보는 x를 1 감소
//         else if (key == "right") ++x;  // 오른쪽 이동 후보는 x를 1 증가
//         else if (key == "up") ++y;  // 위쪽 이동 후보는 y를 1 증가
//         else --y;  // else는 앞선 if 조건이 거짓인 경우의 계산을 실행
//         if (abs(x) <= board[0] / 2 && abs(y) <= board[1] / 2) answer = {x, y};  // 후보가 가로·세로 경계 안에 있을 때만 실제 좌표 갱신
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 이동할 후보 좌표를 먼저 만들고 지도 경계 안에 있을 때만 반영
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120861_%EC%BA%90%EB%A6%AD%ED%84%B0%EC%9D%98_%EC%A2%8C%ED%91%9C/README.md)
