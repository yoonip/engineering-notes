# 정사각형으로 만들기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181830) · Level 0 · C++

## 풀이

행 수와 열 수 중 큰 길이에 맞춰 부족한 열과 행만 0으로 채우기

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

vector<vector<int>> solution(vector<vector<int>> arr) {
    size_t n = max(arr.size(), arr[0].size());
    for (auto& row : arr) row.resize(n, 0);
    arr.resize(n, vector<int>(n, 0));
    return arr;
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
// vector<vector<int>> solution(vector<vector<int>> arr) {  // 정사각형으로 만들기 풀이 시작
//     size_t n = max(arr.size(), arr[0].size());  // 행 수와 열 수 중 큰 쪽을 정사각형의 한 변으로 선택
//     for (auto& row : arr) row.resize(n, 0);  // 각 행의 부족한 열을 0으로 채우기
//     arr.resize(n, vector<int>(n, 0));  // 행이 부족하면 전부 0인 새 행 추가
//     return arr;  // 원래 원소를 유지한 n×n 정사각형
// }  // 블록 끝

// 풀이 요약
// 행 수와 열 수 중 큰 길이에 맞춰 부족한 열과 행만 0으로 채우기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:35
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181830_%EC%A0%95%EC%82%AC%EA%B0%81%ED%98%95%EC%9C%BC%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
