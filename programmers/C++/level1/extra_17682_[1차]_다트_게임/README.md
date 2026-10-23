# [1차] 다트 게임

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/17682) · Level 1 · C++

## 풀이

숫자를 읽어 점수로 만들고 S·D·T에서 거듭제곱 확정. *는 현재·직전 점수를 두 배, #는 현재 점수의 부호 반전.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

int solution(string dartResult) {
    vector<int> scores; int number = 0;
    for (char c : dartResult) {
        if (isdigit((unsigned char)c)) number = number * 10 + c - '0';
        else if (c == 'S' || c == 'D' || c == 'T') { int value = 1, power = c == 'S' ? 1 : c == 'D' ? 2 : 3; for (int i = 0; i < power; ++i) value *= number; scores.push_back(value); number = 0; }
        else if (c == '*') { scores.back() *= 2; if (scores.size() >= 2) scores[scores.size() - 2] *= 2; }
        else if (c == '#') scores.back() *= -1;
    }
    return accumulate(scores.begin(), scores.end(), 0);
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(string dartResult) {  // [1차] 다트 게임 풀이 함수 정의
//     vector<int> scores; int number = 0;  // 회차별 점수 scores와 아직 읽는 기본 숫자 number 준비
//     for (char c : dartResult) {  // 다트 결과의 문자를 순서대로 처리
//         if (isdigit((unsigned char)c)) number = number * 10 + c - '0';  // 숫자이면 10을 곱해 새 자릿수를 이어 붙임. 10점도 두 자리로 처리
//         else if (c == 'S' || c == 'D' || c == 'T') { int value = 1, power = c == 'S' ? 1 : c == 'D' ? 2 : 3; for (int i = 0; i < power; ++i) value *= number; scores.push_back(value); number = 0; }  // S·D·T에 맞춰 1·2·3제곱을 계산해 회차 점수를 추가하고 숫자 초기화
//         else if (c == '*') { scores.back() *= 2; if (scores.size() >= 2) scores[scores.size() - 2] *= 2; }  // 스타상이면 현재 회차와 존재하는 직전 회차의 점수를 두 배로 변경
//         else if (c == '#') scores.back() *= -1;  // 아차상이면 현재 회차 점수에 -1을 곱함
//     }  // 블록 끝
//     return accumulate(scores.begin(), scores.end(), 0);  // 옵션까지 반영된 모든 회차 점수의 합 반환
// }  // 함수 끝
//

// 풀이 요약
// 숫자를 읽어 점수로 만들고 S·D·T에서 거듭제곱 확정. *는 현재·직전 점수를 두 배, #는 현재 점수의 부호 반전.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_17682_%5B1%EC%B0%A8%5D_%EB%8B%A4%ED%8A%B8_%EA%B2%8C%EC%9E%84/README.md)
