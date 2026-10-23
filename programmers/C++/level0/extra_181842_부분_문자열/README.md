# 부분 문자열

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181842) · Level 0 · C++

## 풀이

포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인

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

int solution(string str1, string str2) { return str2.find(str1) != string::npos; }

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
// int solution(string str1, string str2) { return str2.find(str1) != string::npos; }  // 부분 문자열 풀이 시작

// 풀이 요약
// 포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:23:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181842_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4/README.md)
