# 짝지어 제거하기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12973) · Level 2 · C++

## 풀이

문자를 스택에 넣되 끝 문자와 같으면 짝을 제거하고 마지막에 스택이 비었는지 확인

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

int solution(string s) {
    string stack;
    for (char c : s) {
        if (!stack.empty() && stack.back() == c) stack.pop_back();
        else stack.push_back(c);
    }
    return stack.empty();
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// int solution(string s) {  // 스택 끝의 같은 문자와 현재 문자를 함께 제거
// string stack;  // 아직 제거하지 않은 문자를 스택처럼 저장
// for (char c : s) {  // 문자열을 왼쪽부터 읽기
// if (!stack.empty() && stack.back() == c) stack.pop_back();  // 끝 문자와 같으면 인접한 두 문자 제거
// else stack.push_back(c);  // 짝이 없으면 현재 문자 남기기
// }  // 블록 끝
// return stack.empty();  // 모든 문자를 제거했으면 1 반환
// }  // 블록 끝

// 풀이 요약
// 문자를 스택에 넣되 끝 문자와 같으면 짝을 제거하고 마지막에 스택이 비었는지 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/097_12973_%EC%A7%9D%EC%A7%80%EC%96%B4_%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0/README.md)
