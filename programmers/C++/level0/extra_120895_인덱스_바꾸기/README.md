# 인덱스 바꾸기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120895) · Level 0 · C++

## 풀이

string의 두 인덱스에 직접 접근하여 swap으로 문자를 교환한 뒤 바뀐 문자열을 반환

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

string solution(string my_string, int num1, int num2) {
    swap(my_string[num1], my_string[num2]);
    return my_string;
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
// string solution(string my_string, int num1, int num2) {  // 인덱스 바꾸기 풀이 시작
//     swap(my_string[num1], my_string[num2]);  // swap으로 my_string의 num1 위치 문자와 num2 위치 문자를 서로 바꾸기. []는 각 위치의 문자에 접근
//     return my_string;  // return으로 두 위치의 문자만 교환한 my_string을 반환
// }  // 블록 끝

// 풀이 요약
// string의 두 인덱스에 직접 접근하여 swap으로 문자를 교환한 뒤 바뀐 문자열을 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:27:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120895_%EC%9D%B8%EB%8D%B1%EC%8A%A4_%EB%B0%94%EA%BE%B8%EA%B8%B0/README.md)
