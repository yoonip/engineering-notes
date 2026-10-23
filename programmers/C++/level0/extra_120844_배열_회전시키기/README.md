# 배열 회전시키기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120844) · Level 0 · C++

## 풀이

회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮기기

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

vector<int> solution(vector<int> numbers, string direction) {
    if (direction == "right") rotate(numbers.begin(), numbers.end() - 1, numbers.end());
    else rotate(numbers.begin(), numbers.begin() + 1, numbers.end());
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
// vector<int> solution(vector<int> numbers, string direction) {  // 배열 회전시키기 풀이 시작
//     if (direction == "right") rotate(numbers.begin(), numbers.end() - 1, numbers.end());  // rotate는 지정한 중간 위치의 원소가 맨 앞에 오도록 구간을 회전
//     else rotate(numbers.begin(), numbers.begin() + 1, numbers.end());  // rotate는 지정한 중간 위치의 원소가 맨 앞에 오도록 구간을 회전
//     return numbers;  // 지정된 방향으로 한 칸 회전한 배열
// }  // 블록 끝

// 풀이 요약
// 회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮기기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:54:14
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120844_%EB%B0%B0%EC%97%B4_%ED%9A%8C%EC%A0%84%EC%8B%9C%ED%82%A4%EA%B8%B0/README.md)
