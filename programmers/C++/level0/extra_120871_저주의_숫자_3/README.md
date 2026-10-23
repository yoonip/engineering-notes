# 저주의 숫자 3

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120871) · Level 0 · C++

## 풀이

수를 하나씩 늘리며 3의 배수이거나 자릿수에 3이 있으면 건너뛰기. 그렇게 n번 고른 마지막 값 반환

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
    int value = 0;
    for (int i = 0; i < n; ++i) {
        do { ++value; } while (value % 3 == 0 || to_string(value).find('3') != string::npos);
    }
    return value;
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
// int solution(int n) {  // 저주의 숫자 3 풀이 시작
//     int value = 0;  // 조건에 맞는 수만 셌을 때 마지막으로 남긴 값
//     for (int i = 0; i < n; ++i) {  // 사용할 수 있는 수를 n번 고르기
//         do { ++value; } while (value % 3 == 0 || to_string(value).find('3') != string::npos);  // do 블록을 먼저 한 번 실행하고 끝의 while 조건에 따라 반복
//     }  // 블록 끝
//     return value;  // 3의 배수와 숫자 3을 건너뛴 n번째 값
// }  // 블록 끝

// 풀이 요약
// 수를 하나씩 늘리며 3의 배수이거나 자릿수에 3이 있으면 건너뛰기. 그렇게 n번 고른 마지막 값 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120871_%EC%A0%80%EC%A3%BC%EC%9D%98_%EC%88%AB%EC%9E%90_3/README.md)
