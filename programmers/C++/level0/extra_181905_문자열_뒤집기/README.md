# 문자열 뒤집기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181905) · Level 0 · C++

## 풀이

양 끝을 포함한 s부터 e 구간만 뒤집기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
using namespace std;

string solution(string my_string, int s, int e) {
    reverse(my_string.begin() + s, my_string.begin() + e + 1);
    return my_string;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, int s, int e) {  // 문자열 뒤집기 풀이 시작
//     reverse(my_string.begin() + s, my_string.begin() + e + 1);  // 반복자 덧셈으로 s부터 e까지의 반열린 구간을 지정해 reverse로 뒤집기
//     return my_string;  // return으로 구간 변경을 마친 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 양 끝을 포함한 s부터 e 구간만 뒤집기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:58:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181905_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%92%A4%EC%A7%91%EA%B8%B0/README.md)
