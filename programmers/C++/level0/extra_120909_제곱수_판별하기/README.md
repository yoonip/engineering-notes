# 제곱수 판별하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120909) · Level 0 · C++

## 풀이

1부터 제곱근 이하까지 후보를 검사. 후보의 제곱이 n인 경우 1, 끝까지 없으면 2

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
    for (int r = 1; r <= n / r; ++r) if (r * r == n) return 1;
    return 2;
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
// int solution(int n) {  // 제곱수 판별하기 풀이 시작
//     for (int r = 1; r <= n / r; ++r) if (r * r == n) return 1;  // 제곱근 이하의 양의 정수를 검사해 제곱이 n이면 성공
//     return 2;  // 제곱해서 n이 되는 양의 정수가 없음
// }  // 블록 끝

// 풀이 요약
// 1부터 제곱근 이하까지 후보를 검사. 후보의 제곱이 n인 경우 1, 끝까지 없으면 2
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120909_%EC%A0%9C%EA%B3%B1%EC%88%98_%ED%8C%90%EB%B3%84%ED%95%98%EA%B8%B0/README.md)
