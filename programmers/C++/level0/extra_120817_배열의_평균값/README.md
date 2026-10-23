# 배열의 평균값

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120817) · Level 0 · C++

## 풀이

평균은 전체 합을 원소 개수로 나눈 값임

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

double solution(vector<int> numbers) {
    return accumulate(numbers.begin(), numbers.end(), 0.0) / numbers.size();
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
// double solution(vector<int> numbers) {  // 배열의 평균값 풀이 시작
//     return accumulate(numbers.begin(), numbers.end(), 0.0) / numbers.size();  // 합을 실수로 누적한 뒤 원소 수로 나눠 평균 계산
// }  // 블록 끝

// 풀이 요약
// 평균은 전체 합을 원소 개수로 나눈 값임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120817_%EB%B0%B0%EC%97%B4%EC%9D%98_%ED%8F%89%EA%B7%A0%EA%B0%92/README.md)
