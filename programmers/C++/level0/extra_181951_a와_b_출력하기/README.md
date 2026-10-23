# a와 b 출력하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181951) · Level 0 · C++

## 풀이

입력받은 두 정수를 변수 이름과 함께 각각 출력

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << "a = " << a << '\n';
    cout << "b = " << b << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     int a, b;  // 입력 정수 두 개를 담을 변수를 선언
//     cin >> a >> b;  // 입력 연산자 >>로 정수 두 개를 읽기
//     cout << "a = " << a << '\n';  // <<로 첫 변수의 이름과 값을 출력하고 줄을 바꾸기
//     cout << "b = " << b << '\n';  // <<로 두 번째 변수의 이름과 값을 출력하고 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 두 정수를 변수 이름과 함께 각각 출력
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:31:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181951_a%EC%99%80_b_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
