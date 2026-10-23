# 피자 나눠 먹기 (2)

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120815) · Level 0 · C++

## 풀이

총 조각 수가 사람 수와 6 모두의 배수여야 하므로 최소공배수를 이용

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

int solution(int n) {
    int a = n, b = 6;
    while (b) { int r = a % b; a = b; b = r; }
    return n / a;
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
// int solution(int n) {  // 피자 나눠 먹기 (2) 풀이 시작
//     int a = n, b = 6;  // 사람 수와 한 판의 조각 수의 최대공약수를 구할 값
//     while (b) { int r = a % b; a = b; b = r; }  // 유클리드 호제법으로 gcd(n, 6)을 a에 남기기
//     return n / a;  // 최소공배수 n×6/gcd를 한 판의 6조각으로 나눈 판 수
// }  // 블록 끝

// 풀이 요약
// 총 조각 수가 사람 수와 6 모두의 배수여야 하므로 최소공배수를 이용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:06
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120815_%ED%94%BC%EC%9E%90_%EB%82%98%EB%88%A0_%EB%A8%B9%EA%B8%B0_%282%29/README.md)
