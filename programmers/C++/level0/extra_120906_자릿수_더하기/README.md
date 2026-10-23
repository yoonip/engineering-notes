# 자릿수 더하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120906) · Level 0 · C++

## 풀이

n % 10으로 마지막 자릿수를 더하고 n /= 10으로 제거. 수가 0이 될 때까지 반복

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
    int sum = 0;
    while (n) { sum += n % 10; n /= 10; }
    return sum;
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
// int solution(int n) {  // 자릿수 더하기 풀이 시작
//     int sum = 0;  // 떼어 낸 자릿수의 누적 합
//     while (n) { sum += n % 10; n /= 10; }  // 마지막 자릿수를 더한 뒤 10으로 나눠 그 자리를 제거
//     return sum;  // 모든 자릿수의 합
// }  // 블록 끝

// 풀이 요약
// n % 10으로 마지막 자릿수를 더하고 n /= 10으로 제거. 수가 0이 될 때까지 반복
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:37:29
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120906_%EC%9E%90%EB%A6%BF%EC%88%98_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
