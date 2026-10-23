# 배열에서 문자열 대소문자 변환하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181875) · Level 0 · C++

## 풀이

0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환

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

vector<string> solution(vector<string> strArr) {
    for (int i = 0; i < (int)strArr.size(); ++i)
        for (char& c : strArr[i]) c = i % 2 ? toupper((unsigned char)c) : tolower((unsigned char)c);
    return strArr;
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
// vector<string> solution(vector<string> strArr) {  // 배열에서 문자열 대소문자 변환하기 풀이 시작
//     for (int i = 0; i < (int)strArr.size(); ++i)  // 문자열의 인덱스에 따라 변환 방향 선택
//         for (char& c : strArr[i]) c = i % 2 ? toupper((unsigned char)c) : tolower((unsigned char)c);  // 홀수 인덱스의 문자는 대문자, 짝수 인덱스의 문자는 소문자로
//     return strArr;  // 인덱스별 대소문자 변환을 마친 배열
// }  // 블록 끝

// 풀이 요약
// 0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181875_%EB%B0%B0%EC%97%B4%EC%97%90%EC%84%9C_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%8C%80%EC%86%8C%EB%AC%B8%EC%9E%90_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0/README.md)
