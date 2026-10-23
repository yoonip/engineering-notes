# 꼬리 문자열

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181841) · Level 0 · C++

## 풀이

제외 문구가 없는 문자열만 원래 순서대로 이어 붙이기

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

string solution(vector<string> str_list, string ex) {
    string answer;
    for (const string& text : str_list) if (text.find(ex) == string::npos) answer += text;
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
// string solution(vector<string> str_list, string ex) {  // 꼬리 문자열 풀이 시작
//     string answer;  // ex를 포함하지 않는 문자열을 이어 붙일 결과
//     for (const string& text : str_list) if (text.find(ex) == string::npos) answer += text;  // ex가 포함되지 않은 문자열만 이어 붙이기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 제외 문구가 없는 문자열만 원래 순서대로 이어 붙이기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:23:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181841_%EA%BC%AC%EB%A6%AC_%EB%AC%B8%EC%9E%90%EC%97%B4/README.md)
