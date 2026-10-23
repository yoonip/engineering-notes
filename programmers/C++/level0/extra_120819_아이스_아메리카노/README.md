# 아이스 아메리카노

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120819) · Level 0 · C++

## 풀이

아메리카노 한 잔 가격 5500원으로 가진 돈을 나누기. 몫은 최대 잔 수이고 나머지는 구매 후 남는 돈임

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

vector<int> solution(int money) { return {money / 5500, money % 5500}; }

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
// vector<int> solution(int money) { return {money / 5500, money % 5500}; }  // 아이스 아메리카노 풀이 시작

// 풀이 요약
// 아메리카노 한 잔 가격 5500원으로 가진 돈을 나누기. 몫은 최대 잔 수이고 나머지는 구매 후 남는 돈임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:33:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120819_%EC%95%84%EC%9D%B4%EC%8A%A4_%EC%95%84%EB%A9%94%EB%A6%AC%EC%B9%B4%EB%85%B8/README.md)
