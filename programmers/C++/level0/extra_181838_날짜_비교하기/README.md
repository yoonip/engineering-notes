# 날짜 비교하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181838) · Level 0 · C++

## 풀이

연·월·일 순서의 리스트 비교는 날짜의 선후 비교와 같음. 같은 날짜는 0임

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

int solution(vector<int> date1, vector<int> date2) { return date1 < date2; }

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
// int solution(vector<int> date1, vector<int> date2) { return date1 < date2; }  // 날짜 비교하기 풀이 시작

// 풀이 요약
// 연·월·일 순서의 리스트 비교는 날짜의 선후 비교와 같음. 같은 날짜는 0임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181838_%EB%82%A0%EC%A7%9C_%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0/README.md)
