# 대문자로 바꾸기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181877) · Level 0 · C++

## 풀이

각 문자에 toupper를 적용해 전체 문자열을 대문자로 바꾸기

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

string solution(string myString) {
    for (char& c : myString) c = toupper((unsigned char)c);
    return myString;
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
// string solution(string myString) {  // 대문자로 바꾸기 풀이 시작
//     for (char& c : myString) c = toupper((unsigned char)c);  // 각 문자를 대문자로 바꿔 원래 위치에 저장
//     return myString;  // 대문자로 변환한 문자열 반환
// }  // 블록 끝

// 풀이 요약
// 각 문자에 toupper를 적용해 전체 문자열을 대문자로 바꾸기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181877_%EB%8C%80%EB%AC%B8%EC%9E%90%EB%A1%9C_%EB%B0%94%EA%BE%B8%EA%B8%B0/README.md)
