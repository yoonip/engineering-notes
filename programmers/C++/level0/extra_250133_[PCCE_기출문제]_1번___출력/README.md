# [PCCE 기출문제] 1번 / 출력

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250133) · Level 0 · C++

## 풀이

문자열은 이어 붙이고 정수는 덧셈. 첫 줄 문장, 정수 13, 문자열 310을 차례대로 출력

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>

using namespace std;

int main(void) {
    string msg = "Spring is beginning";
    int val1 = 3;
    string val2 = "3";

    cout << msg << endl;
    cout << val1 + 10 << endl;
    cout << val2 + "10" << endl;

    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     string msg = "Spring is beginning";  // 첫 줄에 출력할 문장
//     int val1 = 3;  // 덧셈할 정수 3
//     string val2 = "3";  // 다른 문자열과 이어 붙일 문자 3
//
//     cout << msg << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     cout << val1 + 10 << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     cout << val2 + "10" << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열은 이어 붙이고 정수는 덧셈. 첫 줄 문장, 정수 13, 문자열 310을 차례대로 출력
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_250133_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_1%EB%B2%88___%EC%B6%9C%EB%A0%A5/README.md)
