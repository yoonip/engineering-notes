# 길이에 따른 연산

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181879) · Level 0 · C++

## 풀이

길이에 따라 합계 또는 곱을 선택

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

int solution(vector<int> num_list) {
    if (num_list.size() >= 11) return accumulate(num_list.begin(), num_list.end(), 0);
    return accumulate(num_list.begin(), num_list.end(), 1, multiplies<int>());
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
// int solution(vector<int> num_list) {  // 길이에 따른 연산 풀이 시작
//     if (num_list.size() >= 11) return accumulate(num_list.begin(), num_list.end(), 0);  // 원소가 11개 이상이면 곱 대신 합 반환
//     return accumulate(num_list.begin(), num_list.end(), 1, multiplies<int>());  // accumulate로 전체 원소의 합계 또는 곱을 계산해 반환
// }  // 블록 끝

// 풀이 요약
// 길이에 따라 합계 또는 곱을 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181879_%EA%B8%B8%EC%9D%B4%EC%97%90_%EB%94%B0%EB%A5%B8_%EC%97%B0%EC%82%B0/README.md)
