# 컨트롤 제트

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120853) · Level 0 · C++

## 풀이

공백으로 구분된 토큰을 읽고 숫자이면 합과 가장 최근 숫자를 갱신. Z이면 가장 최근 숫자를 합에서 빼서 직전 덧셈을 취소

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

int solution(string s) {
    istringstream input(s);
    string token;
    int sum = 0, last = 0;
    while (input >> token) {
        if (token == "Z") { sum -= last; last = 0; }
        else { last = stoi(token); sum += last; }
    }
    return sum;
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
// int solution(string s) {  // 컨트롤 제트 풀이 시작
//     istringstream input(s);  // s를 공백 단위로 읽을 스트림 input
//     string token;  // string 변수 token에 현재 읽은 숫자 문자열 또는 Z 명령을 저장
//     int sum = 0, last = 0;  // int 변수 sum에는 취소를 반영한 합을, last에는 가장 최근에 더한 숫자를 저장하며 둘 다 0으로 시작
//     while (input >> token) {  // 스트림 추출 연산자 >>로 다음 token을 읽을 수 있는 동안 숫자와 명령을 입력 순서대로 처리
//         if (token == "Z") { sum -= last; last = 0; }  // token이 Z이면 직전에 더한 last를 sum에서 빼고, 이미 취소한 값이 다시 사용되지 않도록 last를 0으로 초기화
//         else { last = stoi(token); sum += last; }  // 숫자 토큰이면 stoi로 정수로 바꾸어 last에 저장한 뒤 sum에 더하기
//     }  // 블록 끝
//     return sum;  // 모든 숫자와 취소 명령을 반영한 최종 합 sum을 반환
// }  // 블록 끝

// 풀이 요약
// 공백으로 구분된 토큰을 읽고 숫자이면 합과 가장 최근 숫자를 갱신. Z이면 가장 최근 숫자를 합에서 빼서 직전 덧셈을 취소
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:36:14
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120853_%EC%BB%A8%ED%8A%B8%EB%A1%A4_%EC%A0%9C%ED%8A%B8/README.md)
