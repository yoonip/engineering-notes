# 괄호 회전하기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/76502) · Level 2 · C++

## 풀이

모든 회전 시작 위치에서 괄호를 스택으로 검사해 짝이 맞고 남는 괄호가 없는 경우 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
using namespace std;

int solution(string s) {
    string opens = "([{", closes = ")]}";
    int answer = 0;
    for (int offset = 0; offset < (int)s.size(); ++offset) {
        vector<char> stack; bool valid = true;
        for (int i = 0; i < (int)s.size(); ++i) {
            char c = s[(offset + i) % s.size()];
            if (opens.find(c) != string::npos) stack.push_back(c);
            else if (stack.empty() || stack.back() != opens[closes.find(c)]) { valid = false; break; }
            else stack.pop_back();
        }
        if (valid && stack.empty()) ++answer;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(string s) {  // 문자열의 모든 시작 위치에서 괄호 짝 검사
// string opens = "([{", closes = ")]}";  // 여는 괄호와 닫는 괄호를 같은 인덱스로 대응시키기
// int answer = 0;  // 올바른 회전 수 초기화
// for (int offset = 0; offset < (int)s.size(); ++offset) {  // 모든 회전 시작 위치 검사
// vector<char> stack; bool valid = true;  // 괄호 스택과 현재 회전의 유효성 초기화
// for (int i = 0; i < (int)s.size(); ++i) {  // 회전한 문자열을 원형 인덱스로 읽기
// char c = s[(offset + i) % s.size()];  // 현재 회전에서 i번째 문자 구하기
// if (opens.find(c) != string::npos) stack.push_back(c);  // 여는 괄호는 스택에 넣기
// else if (stack.empty() || stack.back() != opens[closes.find(c)]) { valid = false; break; }  // 닫는 괄호와 짝이 맞지 않으면 종료
// else stack.pop_back();  // 짝이 맞은 여는 괄호 제거
// }  // 블록 끝
// if (valid && stack.empty()) ++answer;  // 모든 문자가 맞고 남은 괄호가 없으면 세기
// }  // 블록 끝
// return answer;  // 올바른 괄호열인 회전 수 반환
// }  // 블록 끝

// 풀이 요약
// 모든 회전 시작 위치에서 괄호를 스택으로 검사해 짝이 맞고 남는 괄호가 없는 경우 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:40:05
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/056_76502_%EA%B4%84%ED%98%B8_%ED%9A%8C%EC%A0%84%ED%95%98%EA%B8%B0/README.md)
