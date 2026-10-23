# 직사각형 넓이 구하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120860) · Level 0 · C++

## 풀이

가로는 x의 최댓값-최솟값, 세로는 y의 최댓값-최솟값임

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
    int min_x = dots[0][0], max_x = min_x, min_y = dots[0][1], max_y = min_y;
    for (const auto& dot : dots) {
        min_x = min(min_x, dot[0]); max_x = max(max_x, dot[0]);
        min_y = min(min_y, dot[1]); max_y = max(max_y, dot[1]);
    }
    return (max_x - min_x) * (max_y - min_y);
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
// int solution(vector<vector<int>> dots) {  // 직사각형 넓이 구하기 풀이 시작
//     int min_x = dots[0][0], max_x = min_x, min_y = dots[0][1], max_y = min_y;  // 첫 점을 x·y 좌표의 최소·최대 기준으로 설정
//     for (const auto& dot : dots) {  // 네 꼭짓점의 좌표 범위 확인
//         min_x = min(min_x, dot[0]); max_x = max(max_x, dot[0]);  // 직사각형의 왼쪽·오른쪽 경계 갱신
//         min_y = min(min_y, dot[1]); max_y = max(max_y, dot[1]);  // 직사각형의 아래·위 경계 갱신
//     }  // 블록 끝
//     return (max_x - min_x) * (max_y - min_y);  // 가로 길이와 세로 길이의 곱
// }  // 블록 끝

// 풀이 요약
// 가로는 x의 최댓값-최솟값, 세로는 y의 최댓값-최솟값임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120860_%EC%A7%81%EC%82%AC%EA%B0%81%ED%98%95_%EB%84%93%EC%9D%B4_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
