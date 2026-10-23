# 모음 제거

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120849) · Level 0 · C++

## 풀이

다섯 모음에 속하지 않은 문자와 공백만 유지

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

string solution(string my_string) {
    string answer;
    for (char c : my_string) if (string("aeiou").find(c) == string::npos) answer += c;
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
// string solution(string my_string) {  // 모음 제거 풀이 시작
//     string answer;  // 모음을 제외한 문자와 공백을 모을 결과
//     for (char c : my_string) if (string("aeiou").find(c) == string::npos) answer += c;  // 다섯 모음에 속하지 않는 문자만 원래 순서대로 남기기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 다섯 모음에 속하지 않은 문자와 공백만 유지
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120849_%EB%AA%A8%EC%9D%8C_%EC%A0%9C%EA%B1%B0/README.md)
