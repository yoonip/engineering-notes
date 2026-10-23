# 치킨 쿠폰

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120884) · Level 0 · C++

## 풀이

쿠폰을 치킨으로 바꾸고 서비스 치킨의 쿠폰까지 다시 교환

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

int solution(int chicken) {
    int answer = 0;
    while (chicken >= 10) {
        int free_chicken = chicken / 10;
        answer += free_chicken;
        chicken = free_chicken + chicken % 10;
    }
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
// int solution(int chicken) {  // 치킨 쿠폰 풀이 시작
//     int answer = 0;  // 쿠폰으로 받은 서비스 치킨 수
//     while (chicken >= 10) {  // 남은 쿠폰 열 장으로 교환할 수 있는 동안 반복
//         int free_chicken = chicken / 10;  // 이번 교환으로 받을 서비스 치킨 수
//         answer += free_chicken;  // 이번에 받은 서비스 치킨을 총수에 추가
//         chicken = free_chicken + chicken % 10;  // 새 치킨에서 받은 쿠폰과 교환 후 남은 쿠폰 합치기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 쿠폰을 치킨으로 바꾸고 서비스 치킨의 쿠폰까지 다시 교환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:14
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120884_%EC%B9%98%ED%82%A8_%EC%BF%A0%ED%8F%B0/README.md)
