# 배열 두 배 만들기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120809) · Level 0 · C++

## 풀이

범위 기반 for문으로 입력 vector의 각 원소를 참조하여 두 배로 바꾼 뒤 그 vector를 반환

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

vector<int> solution(vector<int> numbers) {
    for (int& value : numbers) value *= 2;
    return numbers;
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
// vector<int> solution(vector<int> numbers) {  // 배열 두 배 만들기 풀이 시작
//     for (int& value : numbers) value *= 2;  // 범위 기반 for문으로 numbers의 원소를 int& 참조 value에 연결. 복합 대입 연산자 *=로 각 원소 자체를 두 배로 바꾸기
//     return numbers;  // 모든 원소가 두 배로 바뀐 numbers를 반환
// }  // 블록 끝

// 풀이 요약
// 범위 기반 for문으로 입력 vector의 각 원소를 참조하여 두 배로 바꾼 뒤 그 vector를 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:34:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120809_%EB%B0%B0%EC%97%B4_%EB%91%90_%EB%B0%B0_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
