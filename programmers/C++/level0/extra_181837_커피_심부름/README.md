# 커피 심부름

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181837) · Level 0 · C++

## 풀이

온도에 따라 가격이 바뀌지 않으며 아무거나 주문은 아메리카노 가격임

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(vector<string> order) {
    int total = 0;
    for (const string& item : order) total += item.find("cafelatte") != string::npos ? 5000 : 4500;
    return total;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<string> order) {  // 커피 심부름 풀이 시작
//     int total = 0;  // 전체 주문의 커피 가격 합
//     for (const string& item : order) total += item.find("cafelatte") != string::npos ? 5000 : 4500;  // 카페라테는 5000원, 나머지는 아메리카노 가격 4500원
//     return total;  // 전체 합계 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 온도에 따라 가격이 바뀌지 않으며 아무거나 주문은 아메리카노 가격임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181837_%EC%BB%A4%ED%94%BC_%EC%8B%AC%EB%B6%80%EB%A6%84/README.md)
