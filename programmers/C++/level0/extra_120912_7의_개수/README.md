# 7의 개수

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120912) · Level 0 · C++

## 풀이

각 정수를 문자열로 바꿔 숫자 문자 7의 출현 횟수를 세기

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

int solution(vector<int> array) {
    int answer = 0;
    for (int value : array)
        for (char digit : to_string(value)) answer += digit == '7';
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
// int solution(vector<int> array) {  // 7의 개수 풀이 시작
//     int answer = 0;  // 모든 정수의 자릿수에 나타난 7의 개수
//     for (int value : array)  // 배열의 정수를 하나씩 숫자 문자열로 바꾸기
//         for (char digit : to_string(value)) answer += digit == '7';  // 숫자 문자가 7일 때마다 하나씩 세기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 정수를 문자열로 바꿔 숫자 문자 7의 출현 횟수를 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:29
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120912_7%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
