# 점의 위치 구하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120841) · Level 0 · C++

## 풀이

x 좌표의 양수 여부로 오른쪽과 왼쪽을 나누고, 각 경우에서 y 좌표의 양수 여부로 사분면을 결정

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

int solution(vector<int> dot) {
    return dot[0] > 0 ? (dot[1] > 0 ? 1 : 4) : (dot[1] > 0 ? 2 : 3);
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
// int solution(vector<int> dot) {  // 점의 위치 구하기 풀이 시작
//     return dot[0] > 0 ? (dot[1] > 0 ? 1 : 4) : (dot[1] > 0 ? 2 : 3);  // 중첩 삼항 연산자로 x가 양수이면 y의 부호에 따라 1 또는 4를, x가 음수이면 y의 부호에 따라 2 또는 3을 반환
// }  // 블록 끝

// 풀이 요약
// x 좌표의 양수 여부로 오른쪽과 왼쪽을 나누고, 각 경우에서 y 좌표의 양수 여부로 사분면을 결정
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:31:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120841_%EC%A0%90%EC%9D%98_%EC%9C%84%EC%B9%98_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
