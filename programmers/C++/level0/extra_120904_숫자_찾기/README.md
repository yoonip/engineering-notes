# 숫자 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120904) · Level 0 · C++

## 풀이

정수를 문자열로 바꾸어 숫자 문자의 첫 위치를 찾기

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

int solution(int num, int k) {
    size_t pos = to_string(num).find(char('0' + k));
    return pos == string::npos ? -1 : static_cast<int>(pos) + 1;
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
// int solution(int num, int k) {  // 숫자 찾기 풀이 시작
//     size_t pos = to_string(num).find(char('0' + k));  // 숫자 k를 문자로 바꿔 처음 나오는 위치 검색
//     return pos == string::npos ? -1 : static_cast<int>(pos) + 1;  // 없으면 -1, 있으면 1부터 세는 자릿수 위치
// }  // 블록 끝

// 풀이 요약
// 정수를 문자열로 바꾸어 숫자 문자의 첫 위치를 찾기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:37:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120904_%EC%88%AB%EC%9E%90_%EC%B0%BE%EA%B8%B0/README.md)
