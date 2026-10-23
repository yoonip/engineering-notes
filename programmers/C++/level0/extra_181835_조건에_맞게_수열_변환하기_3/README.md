# 조건에 맞게 수열 변환하기 3

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181835) · Level 0 · C++

## 풀이

각 원소에 k가 홀수이면 곱셈을, 짝수이면 덧셈을 적용

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

vector<int> solution(vector<int> arr, int k) {
    for (int& value : arr) value = k % 2 ? value * k : value + k;
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
// vector<int> solution(vector<int> arr, int k) {  // 조건에 맞게 수열 변환하기 3 풀이 시작
//     for (int& value : arr) value = k % 2 ? value * k : value + k;  // k가 홀수면 각 값에 곱하고 짝수면 더하기
//     return arr;  // k의 홀짝에 따른 변환을 끝낸 배열
// }  // 블록 끝

// 풀이 요약
// 각 원소에 k가 홀수이면 곱셈을, 짝수이면 덧셈을 적용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:26:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181835_%EC%A1%B0%EA%B1%B4%EC%97%90_%EB%A7%9E%EA%B2%8C_%EC%88%98%EC%97%B4_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0_3/README.md)
