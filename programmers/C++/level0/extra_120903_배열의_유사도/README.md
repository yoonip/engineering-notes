# 배열의 유사도

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120903) · Level 0 · C++

## 풀이

s1의 각 문자열을 s2에서 find로 검색하고, 발견한 경우마다 개수를 1씩 더해 두 배열의 공통 문자열 수를 구하기

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

int solution(vector<string> s1, vector<string> s2) {
    int answer = 0;
    for (const string& word : s1) answer += find(s2.begin(), s2.end(), word) != s2.end();
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
// int solution(vector<string> s1, vector<string> s2) {  // 배열의 유사도 풀이 시작
//     int answer = 0;  // int 변수 answer를 0으로 초기화하여 공통 문자열의 개수를 세기
//     for (const string& word : s1) answer += find(s2.begin(), s2.end(), word) != s2.end();  // 범위 기반 for로 s1의 각 word를 const 참조로 읽기. find로 s2 전체에서 word를 찾고, 끝 반복자와 다르면 존재한다는 뜻이므로 answer에 1을 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// s1의 각 문자열을 s2에서 find로 검색하고, 발견한 경우마다 개수를 1씩 더해 두 배열의 공통 문자열 수를 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:26:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120903_%EB%B0%B0%EC%97%B4%EC%9D%98_%EC%9C%A0%EC%82%AC%EB%8F%84/README.md)
