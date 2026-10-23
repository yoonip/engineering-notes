# 수열과 구간 쿼리 1

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181883) · Level 0 · C++

## 풀이

각 닫힌 구간에 속한 원소를 모두 1씩 증가

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

vector<int> solution(vector<int> arr, vector<vector<int>> queries) {
    for (const auto& q : queries)
        for (int i = q[0]; i <= q[1]; ++i) ++arr[i];
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
// vector<int> solution(vector<int> arr, vector<vector<int>> queries) {  // 수열과 구간 쿼리 1 풀이 시작
//     for (const auto& q : queries)  // 입력된 구간 쿼리를 순서대로 적용
//         for (int i = q[0]; i <= q[1]; ++i) ++arr[i];  // 쿼리의 양 끝을 포함한 모든 원소를 1 증가
//     return arr;  // 모든 구간의 증가를 반영한 배열 반환
// }  // 블록 끝

// 풀이 요약
// 각 닫힌 구간에 속한 원소를 모두 1씩 증가
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:07:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181883_%EC%88%98%EC%97%B4%EA%B3%BC_%EA%B5%AC%EA%B0%84_%EC%BF%BC%EB%A6%AC_1/README.md)
