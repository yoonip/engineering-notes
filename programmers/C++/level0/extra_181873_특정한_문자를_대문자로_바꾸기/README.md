# 특정한 문자를 대문자로 바꾸기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181873) · Level 0 · C++

## 풀이

지정된 문자만 대문자로 치환

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

string solution(string my_string, string alp) {
    for (char& c : my_string) if (c == alp[0]) c = toupper((unsigned char)c);
    return my_string;
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
// string solution(string my_string, string alp) {  // 특정한 문자를 대문자로 바꾸기 풀이 시작
//     for (char& c : my_string) if (c == alp[0]) c = toupper((unsigned char)c);  // 지정한 alp 문자와 일치하는 위치만 대문자로
//     return my_string;  // 대상 문자만 바꾼 문자열
// }  // 블록 끝

// 풀이 요약
// 지정된 문자만 대문자로 치환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:10:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181873_%ED%8A%B9%EC%A0%95%ED%95%9C_%EB%AC%B8%EC%9E%90%EB%A5%BC_%EB%8C%80%EB%AC%B8%EC%9E%90%EB%A1%9C_%EB%B0%94%EA%BE%B8%EA%B8%B0/README.md)
