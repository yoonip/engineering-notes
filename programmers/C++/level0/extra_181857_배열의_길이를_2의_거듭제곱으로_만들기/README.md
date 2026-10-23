# 배열의 길이를 2의 거듭제곱으로 만들기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181857) · Level 0 · C++

## 풀이

현재 길이 이상인 가장 작은 2의 거듭제곱을 찾고 그 차이만큼 0을 추가

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

vector<int> solution(vector<int> arr) {
    size_t length = 1;
    while (length < arr.size()) length *= 2;
    arr.resize(length, 0);
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
// vector<int> solution(vector<int> arr) {  // 배열의 길이를 2의 거듭제곱으로 만들기 풀이 시작
//     size_t length = 1;  // 늘릴 길이의 후보인 가장 작은 2의 거듭제곱
//     while (length < arr.size()) length *= 2;  // 원래 길이 이상이 될 때까지 후보 길이를 두 배씩 증가
//     arr.resize(length, 0);  // 원소는 유지하고 새로 늘어난 뒷부분만 0으로 채우기
//     return arr;  // 길이가 2의 거듭제곱이 된 배열
// }  // 블록 끝

// 풀이 요약
// 현재 길이 이상인 가장 작은 2의 거듭제곱을 찾고 그 차이만큼 0을 추가
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181857_%EB%B0%B0%EC%97%B4%EC%9D%98_%EA%B8%B8%EC%9D%B4%EB%A5%BC_2%EC%9D%98_%EA%B1%B0%EB%93%AD%EC%A0%9C%EA%B3%B1%EC%9C%BC%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
