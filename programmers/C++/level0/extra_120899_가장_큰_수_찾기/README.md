# 가장 큰 수 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120899) · Level 0 · C++

## 풀이

max_element로 최댓값의 반복자를 구하기. 반복자의 값과 배열 시작으로부터의 거리를 각각 최댓값과 0부터 시작하는 인덱스로 반환

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

vector<int> solution(vector<int> array) {
    auto position = max_element(array.begin(), array.end());
    return {*position, static_cast<int>(position - array.begin())};
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
// vector<int> solution(vector<int> array) {  // 가장 큰 수 찾기 풀이 시작
//     auto position = max_element(array.begin(), array.end());  // max_element로 배열 전체에서 최댓값이 있는 위치를 찾기. auto는 반환된 반복자의 자료형을 추론하여 position에 저장
//     return {*position, static_cast<int>(position - array.begin())};  // 찾은 최댓값과 시작 반복자부터의 거리인 인덱스를 함께 반환
// }  // 블록 끝

// 풀이 요약
// max_element로 최댓값의 반복자를 구하기. 반복자의 값과 배열 시작으로부터의 거리를 각각 최댓값과 0부터 시작하는 인덱스로 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:26:35
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120899_%EA%B0%80%EC%9E%A5_%ED%81%B0_%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
