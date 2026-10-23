# 평행

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120875) · Level 0 · C++

## 풀이

기울기의 분자·분모를 교차 곱해 비교하고 네 점을 두 쌍으로 나누는 모든 경우를 검사

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

int solution(vector<vector<int>> dots) {
    int pairs[3][4] = {{0,1,2,3}, {0,2,1,3}, {0,3,1,2}};
    for (const auto& p : pairs) {
        long long dx1 = dots[p[1]][0] - dots[p[0]][0], dy1 = dots[p[1]][1] - dots[p[0]][1];
        long long dx2 = dots[p[3]][0] - dots[p[2]][0], dy2 = dots[p[3]][1] - dots[p[2]][1];
        if (dy1 * dx2 == dy2 * dx1) return 1;
    }
    return 0;
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
// int solution(vector<vector<int>> dots) {  // 평행 풀이 시작
//     int pairs[3][4] = {{0,1,2,3}, {0,2,1,3}, {0,3,1,2}};  // pairs[3][4] = {{0를 저장할 변수 · 1를 저장할 변수 · 2를 저장할 변수 · 3}를 저장할 변수 · {0를 저장할 변수 · 2를 저장할 변수 · 1를 저장할 변수 · 3}를 저장할 변수 · {0를 저장할 변수 · 3를 저장할 변수 · 1를 저장할 변수 · 2}}를 저장할 변수
//     for (const auto& p : pairs) {  // 네 점을 서로 다른 두 쌍으로 나누는 세 경우
//         long long dx1 = dots[p[1]][0] - dots[p[0]][0], dy1 = dots[p[1]][1] - dots[p[0]][1];  // 첫 직선의 가로·세로 변화량
//         long long dx2 = dots[p[3]][0] - dots[p[2]][0], dy2 = dots[p[3]][1] - dots[p[2]][1];  // 두 번째 직선의 가로·세로 변화량
//         if (dy1 * dx2 == dy2 * dx1) return 1;  // if 조건이 참이면 지정한 결과를 즉시 반환하여 함수 실행을 끝
//     }  // 블록 끝
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝

// 풀이 요약
// 기울기의 분자·분모를 교차 곱해 비교하고 네 점을 두 쌍으로 나누는 모든 경우를 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:06
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120875_%ED%8F%89%ED%96%89/README.md)
