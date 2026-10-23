# 큰 수 만들기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42883) · Level 2 · C++

## 풀이

새 자릿수보다 작은 스택 끝 숫자를 제거해 큰 자릿수가 앞에 오게 만들고 남은 제거 횟수는 뒤에서 사용

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
using namespace std;

string solution(string number, int k) {
    string stack;
    for (char digit : number) {
        while (k > 0 && !stack.empty() && stack.back() < digit) { stack.pop_back(); --k; }
        stack.push_back(digit);
    }
    if (k > 0) stack.resize(stack.size() - k);
    return stack;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(string number, int k) {  // 작은 앞자리를 지워 남는 수 최대화
// string stack;  // 큰 자릿수부터 유지할 숫자를 스택처럼 저장
// for (char digit : number) {  // 숫자를 왼쪽부터 읽기
// while (k > 0 && !stack.empty() && stack.back() < digit) { stack.pop_back(); --k; }  // 더 큰 숫자를 앞으로 보내도록 작은 끝 숫자 제거
// stack.push_back(digit);  // 현재 숫자를 뒤에 넣기
// }  // 블록 끝
// if (k > 0) stack.resize(stack.size() - k);  // 제거 횟수가 남으면 작은 뒤쪽 자릿수 지우기
// return stack;  // 만들 수 있는 가장 큰 수 반환
// }  // 블록 끝

// 풀이 요약
// 새 자릿수보다 작은 스택 끝 숫자를 제거해 큰 자릿수가 앞에 오게 만들고 남은 제거 횟수는 뒤에서 사용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:21:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/073_42883_%ED%81%B0_%EC%88%98_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
