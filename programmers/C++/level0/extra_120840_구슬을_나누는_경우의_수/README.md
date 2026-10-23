# 구슬을 나누는 경우의 수

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120840) · Level 0 · C++

## 풀이

구슬을 고르는 순서를 고려하지 않으므로 조합 nCk를 사용

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

int solution(int balls, int share) {
    share = min(share, balls - share);
    long long answer = 1;
    for (int i = 1; i <= share; ++i) answer = answer * (balls - share + i) / i;
    return static_cast<int>(answer);
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
// int solution(int balls, int share) {  // 구슬을 나누는 경우의 수 풀이 시작
//     share = min(share, balls - share);  // 조합의 대칭성을 이용해 더 적은 개수를 고르는 쪽으로 계산
//     long long answer = 1;  // 곱셈·나눗셈으로 누적할 조합 수
//     for (int i = 1; i <= share; ++i) answer = answer * (balls - share + i) / i;  // 분자 항을 하나 곱하고 i로 나누며 조합 수 누적
//     return static_cast<int>(answer);  // 계산한 조합 수를 요구한 int형으로 반환
// }  // 블록 끝

// 풀이 요약
// 구슬을 고르는 순서를 고려하지 않으므로 조합 nCk를 사용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120840_%EA%B5%AC%EC%8A%AC%EC%9D%84_%EB%82%98%EB%88%84%EB%8A%94_%EA%B2%BD%EC%9A%B0%EC%9D%98_%EC%88%98/README.md)
