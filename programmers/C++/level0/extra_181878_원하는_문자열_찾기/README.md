# 원하는 문자열 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181878) · Level 0 · C++

## 풀이

양쪽 문자열을 모두 소문자로 바꿔 대소문자를 구분하지 않고 찾기

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

int solution(string myString, string pat) {
    for (char& c : myString) c = tolower((unsigned char)c);
    for (char& c : pat) c = tolower((unsigned char)c);
    return myString.find(pat) != string::npos;
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
// int solution(string myString, string pat) {  // 원하는 문자열 찾기 풀이 시작
//     for (char& c : myString) c = tolower((unsigned char)c);  // 검색 대상 문자열을 소문자로 통일
//     for (char& c : pat) c = tolower((unsigned char)c);  // 찾을 패턴도 소문자로 통일
//     return myString.find(pat) != string::npos;  // 검색 결과가 존재하는지 비교해 참이면 1, 거짓이면 0을 반환
// }  // 블록 끝

// 풀이 요약
// 양쪽 문자열을 모두 소문자로 바꿔 대소문자를 구분하지 않고 찾기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181878_%EC%9B%90%ED%95%98%EB%8A%94_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%B0%BE%EA%B8%B0/README.md)
