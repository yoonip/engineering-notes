# 조건에 맞게 수열 변환하기 1

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181882) · Level 0 · C++

## 풀이

50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 그대로 두기

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
    for (int& value : arr) {
        if (value >= 50 && value % 2 == 0) value /= 2;
        else if (value < 50 && value % 2) value *= 2;
    }
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
// vector<int> solution(vector<int> arr) {  // 조건에 맞게 수열 변환하기 1 풀이 시작
//     for (int& value : arr) {  // 원소를 참조해 조건에 맞는 값만 제자리에서 변환
//         if (value >= 50 && value % 2 == 0) value /= 2;  // value >= 50 && value % 2 == 0이면 value에 2 나누기
//         else if (value < 50 && value % 2) value *= 2;  // 50 미만인 홀수는 두 배
//     }  // 블록 끝
//     return arr;  // 조건에 맞게 변환한 배열 반환
// }  // 블록 끝

// 풀이 요약
// 50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 그대로 두기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:08:05
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181882_%EC%A1%B0%EA%B1%B4%EC%97%90_%EB%A7%9E%EA%B2%8C_%EC%88%98%EC%97%B4_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0_1/README.md)
