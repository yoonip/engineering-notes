# 문자열 정렬하기 (2)

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120911) · Level 0 · C++

## 풀이

소문자로 통일한 후 각 문자를 정렬해 다시 연결

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
    for (char& c : my_string) c = tolower(static_cast<unsigned char>(c));
    sort(my_string.begin(), my_string.end());
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
// string solution(string my_string) {  // 문자열 정렬하기 (2) 풀이 시작
//     for (char& c : my_string) c = tolower(static_cast<unsigned char>(c));  // 모든 영문자를 소문자로 통일
//     sort(my_string.begin(), my_string.end());  // my_string를 오름차순 정렬
//     return my_string;  // 소문자로 바꿔 정렬한 문자열
// }  // 블록 끝

// 풀이 요약
// 소문자로 통일한 후 각 문자를 정렬해 다시 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120911_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%A0%95%EB%A0%AC%ED%95%98%EA%B8%B0_%282%29/README.md)
