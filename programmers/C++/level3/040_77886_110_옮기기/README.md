# 110 옮기기

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77886) · Level 3 · C++

## 풀이

스택으로 모든 110 묶음을 제거한 뒤 남은 문자열의 마지막 0 뒤에 묶음을 넣어 사전순으로 최소화

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

vector<string> solution(vector<string> s) {
    vector<string> answer;
    for (const string& word : s) {
        string stack; int count = 0;
        for (char c : word) {
            stack += c;
            if (stack.size() >= 3 && stack.compare(stack.size() - 3, 3, "110") == 0) { stack.resize(stack.size() - 3); ++count; }
        }
        size_t last_zero = stack.rfind('0'), index = last_zero == string::npos ? 0 : last_zero + 1;
        string middle; middle.reserve(3 * count); for (int i = 0; i < count; ++i) middle += "110";
        answer.push_back(stack.substr(0, index) + middle + stack.substr(index));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<string> solution(vector<string> s) {  // 110을 모두 꺼낸 뒤 사전순 최소 위치에 삽입
// vector<string> answer;  // 각 문자열의 최소 결과 저장
// for (const string& word : s) {  // 이진 문자열을 하나씩 처리
// string stack; int count = 0;  // 110을 제거한 나머지와 제거 횟수 저장
// for (char c : word) {  // 문자를 순서대로 스택에 넣기
// stack += c;  // 현재 문자 추가
// if (stack.size() >= 3 && stack.compare(stack.size() - 3, 3, "110") == 0) { stack.resize(stack.size() - 3); ++count; }  // 끝의 110을 발견하면 제거해 따로 세기
// }  // 블록 끝
// size_t last_zero = stack.rfind('0'), index = last_zero == string::npos ? 0 : last_zero + 1;  // 남은 마지막 0 바로 뒤를 삽입 위치로 정하기
// string middle; middle.reserve(3 * count); for (int i = 0; i < count; ++i) middle += "110";  // 제거한 110 묶음을 다시 만들기
// answer.push_back(stack.substr(0, index) + middle + stack.substr(index));  // 마지막 0 뒤와 남은 1들 앞에 묶음 넣기
// }  // 블록 끝
// return answer;  // 사전순으로 최소화한 문자열들 반환
// }  // 블록 끝

// 풀이 요약
// 스택으로 모든 110 묶음을 제거한 뒤 남은 문자열의 마지막 0 뒤에 묶음을 넣어 사전순으로 최소화
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/040_77886_110_%EC%98%AE%EA%B8%B0%EA%B8%B0/README.md)
