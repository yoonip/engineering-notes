# 특정 문자열로 끝나는 가장 긴 부분 문자열 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181872) · Level 0 · C++

## 풀이

가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열임

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

string solution(string myString, string pat) {
    return myString.substr(0, myString.rfind(pat) + pat.size());
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
// string solution(string myString, string pat) {  // 특정 문자열로 끝나는 가장 긴 부분 문자열 찾기 풀이 시작
//     return myString.substr(0, myString.rfind(pat) + pat.size());  // 검색 결과가 존재하는지 비교해 참이면 1, 거짓이면 0을 반환
// }  // 블록 끝

// 풀이 요약
// 가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열임
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:10:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181872_%ED%8A%B9%EC%A0%95_%EB%AC%B8%EC%9E%90%EC%97%B4%EB%A1%9C_%EB%81%9D%EB%82%98%EB%8A%94_%EA%B0%80%EC%9E%A5_%EA%B8%B4_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%B0%BE%EA%B8%B0/README.md)
