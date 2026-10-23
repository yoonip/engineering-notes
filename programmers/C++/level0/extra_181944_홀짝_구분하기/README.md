# 홀짝 구분하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181944) · Level 0 · C++

## 풀이

2로 나눈 나머지에 따라 짝수와 홀수 출력 형식을 선택

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    cout << n << " is " << (n % 2 == 0 ? "even" : "odd") << '\n';
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
// int main() {  // 입력을 읽고 답을 출력할 시작점
//     int n;  // 입력받을 정수를 저장할 int형 변수를 선언
//     cin >> n;  // 입력 연산자 >>로 정수 n을 읽기
//     cout << n << " is " << (n % 2 == 0 ? "even" : "odd") << '\n';  // 나머지 연산자 %와 삼항 연산자 ?:로 홀짝을 구분하고 <<로 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 2로 나눈 나머지에 따라 짝수와 홀수 출력 형식을 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:32:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181944_%ED%99%80%EC%A7%9D_%EA%B5%AC%EB%B6%84%ED%95%98%EA%B8%B0/README.md)
