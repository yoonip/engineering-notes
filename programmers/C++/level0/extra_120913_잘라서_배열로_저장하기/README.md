# 잘라서 배열로 저장하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120913) · Level 0 · C++

## 풀이

시작 위치를 n칸씩 옮기며 최대 n글자씩 자르기. 마지막 조각은 남은 문자만 포함

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

vector<string> solution(string my_str, int n) {
    vector<string> answer;
    for (size_t i = 0; i < my_str.size(); i += n) answer.push_back(my_str.substr(i, n));
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
// vector<string> solution(string my_str, int n) {  // 잘라서 배열로 저장하기 풀이 시작
//     vector<string> answer;  // n글자씩 나눈 문자열 조각
//     for (size_t i = 0; i < my_str.size(); i += n) answer.push_back(my_str.substr(i, n));  // 시작점을 n칸씩 옮기며 최대 n글자씩 잘라 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작 위치를 n칸씩 옮기며 최대 n글자씩 자르기. 마지막 조각은 남은 문자만 포함
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120913_%EC%9E%98%EB%9D%BC%EC%84%9C_%EB%B0%B0%EC%97%B4%EB%A1%9C_%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0/README.md)
