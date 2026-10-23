# 문자열 여러 번 뒤집기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181913) · Level 0 · C++

## 풀이

쿼리 순서대로 각 구간의 양 끝 문자를 교환하며 뒤집기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
#include <vector>
using namespace std;

string solution(string my_string, vector<vector<int>> queries) {
    for (const auto& query : queries) reverse(my_string.begin() + query[0], my_string.begin() + query[1] + 1);
    return my_string;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// string solution(string my_string, vector<vector<int>> queries) {  // 문자열 여러 번 뒤집기 풀이 시작
//     for (const auto& query : queries) reverse(my_string.begin() + query[0], my_string.begin() + query[1] + 1);  // 범위 for로 쿼리를 const 참조로 읽고 reverse로 양 끝을 포함하는 범위를 뒤집기
//     return my_string;  // return으로 구간 변경을 마친 문자열을 반환
// }  // 블록 끝

// 풀이 요약
// 쿼리 순서대로 각 구간의 양 끝 문자를 교환하며 뒤집기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:55:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181913_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%97%AC%EB%9F%AC_%EB%B2%88_%EB%92%A4%EC%A7%91%EA%B8%B0/README.md)
