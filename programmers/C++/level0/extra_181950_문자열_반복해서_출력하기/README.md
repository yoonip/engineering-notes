# 문자열 반복해서 출력하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181950) · Level 0 · C++

## 풀이

문자열을 n번 출력하고 마지막에 줄을 바꾸기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>
#include <string>
using namespace std;
int main() {
    string text;
    int n;
    cin >> text >> n;
    for (int i = 0; i < n; ++i) cout << text;
    cout << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// #include <string>  // 문자열을 다룰 string
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     string text;  // 입력 문자열을 저장할 변수를 선언
//     int n;  // 반복 횟수를 저장할 int형 변수를 선언
//     cin >> text >> n;  // 입력 연산자 >>로 문자열과 정수를 읽기
//     for (int i = 0; i < n; ++i) cout << text;  // for로 n번 반복하며 <<로 문자열을 이어 출력
//     cout << '\n';  // 마지막에 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열을 n번 출력하고 마지막에 줄을 바꾸기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:31:38
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181950_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%B0%98%EB%B3%B5%ED%95%B4%EC%84%9C_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
