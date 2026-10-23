# 세 개의 구분자

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181862) · Level 0 · C++

## 풀이

a·b·c를 공백으로 바꾼 뒤 입력 스트림으로 단어를 읽기. 연속 구분자와 양 끝의 빈 조각은 자동으로 건너뛰기

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

vector<string> solution(string myStr) {
    for (char& c : myStr) if (c == 'a' || c == 'b' || c == 'c') c = ' ';
    istringstream stream(myStr);
    vector<string> answer;
    string part;
    while (stream >> part) answer.push_back(part);
    if (answer.empty()) answer.push_back("EMPTY");
    return answer;
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
// vector<string> solution(string myStr) {  // 세 개의 구분자 풀이 시작
//     for (char& c : myStr) if (c == 'a' || c == 'b' || c == 'c') c = ' ';  // 세 구분자 a·b·c를 공백으로 통일
//     istringstream stream(myStr);  // myStr를 공백 단위로 읽을 스트림 stream
//     vector<string> answer;  // a·b·c 사이에서 나온 단어 목록
//     string part;  // 구분자 사이에서 읽은 현재 단어
//     while (stream >> part) answer.push_back(part);  // 연속 구분자로 생긴 빈 조각은 건너뛰고 단어만 추가
//     if (answer.empty()) answer.push_back("EMPTY");  // if로 조건을 검사하고 push_back으로 해당 원소를 결과 뒤에 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// a·b·c를 공백으로 바꾼 뒤 입력 스트림으로 단어를 읽기. 연속 구분자와 양 끝의 빈 조각은 자동으로 건너뛰기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:43
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181862_%EC%84%B8_%EA%B0%9C%EC%9D%98_%EA%B5%AC%EB%B6%84%EC%9E%90/README.md)
