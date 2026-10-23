# 문자열 붙여서 출력하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181946) · Level 0 · C++

## 풀이

공백으로 구분한 두 문자열을 붙여 출력

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string first, second;
    cin >> first >> second;
    cout << first << second << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     string first, second;  // 입력 문자열 두 개를 저장할 변수를 선언
//     cin >> first >> second;  // 공백으로 구분된 문자열 두 개를 >>로 읽기
//     cout << first << second << '\n';  // 출력 연산자 <<로 두 문자열을 공백 없이 붙이고 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 공백으로 구분한 두 문자열을 붙여 출력
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:32:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181946_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%B6%99%EC%97%AC%EC%84%9C_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
