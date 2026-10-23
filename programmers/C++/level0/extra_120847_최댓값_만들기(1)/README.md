# 최댓값 만들기(1)

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120847) · Level 0 · C++

## 풀이

모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대임

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

int solution(vector<int> numbers) {
    sort(numbers.begin(), numbers.end(), greater<int>());
    return numbers[0] * numbers[1];
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
// int solution(vector<int> numbers) {  // 최댓값 만들기(1) 풀이 시작
//     sort(numbers.begin(), numbers.end(), greater<int>());  // 정렬 함수와 greater 비교자로 배열을 내림차순으로 정렬
//     return numbers[0] * numbers[1];  // 내림차순으로 정렬한 가장 큰 두 원소의 곱
// }  // 블록 끝

// 풀이 요약
// 모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120847_%EC%B5%9C%EB%8C%93%EA%B0%92_%EB%A7%8C%EB%93%A4%EA%B8%B0%281%29/README.md)
