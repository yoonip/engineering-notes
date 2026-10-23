# 분수의 덧셈

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120808) · Level 0 · C++

## 풀이

통분하여 더한 뒤 최대공약수로 분자와 분모를 나누어 약분

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

int gcd_value(int a, int b) {
    while (b) { int r = a % b; a = b; b = r; }
    return a;
}
vector<int> solution(int numer1, int denom1, int numer2, int denom2) {
    int n = numer1 * denom2 + numer2 * denom1, d = denom1 * denom2;
    int g = gcd_value(n, d);
    return {n / g, d / g};
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
// int gcd_value(int a, int b) {  // 두 정수의 최대공약수를 구하는 정수형 보조 함수를 정의
//     while (b) { int r = a % b; a = b; b = r; }  // 나머지를 반복해서 최대공약수 구하기
//     return a;  // 마지막으로 남은 최대공약수
// }  // 블록 끝
// vector<int> solution(int numer1, int denom1, int numer2, int denom2) {  // 분수의 덧셈 풀이 시작
//     int n = numer1 * denom2 + numer2 * denom1, d = denom1 * denom2;  // 통분해서 더한 분자와 공통 분모
//     int g = gcd_value(n, d);  // 합한 분자와 분모를 약분할 최대공약수
//     return {n / g, d / g};  // 기약분수의 분자와 분모를 순서대로 반환
// }  // 블록 끝

// 풀이 요약
// 통분하여 더한 뒤 최대공약수로 분자와 분모를 나누어 약분
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:54:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120808_%EB%B6%84%EC%88%98%EC%9D%98_%EB%8D%A7%EC%85%88/README.md)
