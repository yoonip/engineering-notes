# [PCCE 기출문제] 2번 / 피타고라스의 정리

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250132) · Level 0 · C++

## 풀이

피타고라스 정리의 b² = c² - a²를 계산

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>

using namespace std;

int main(void) {
    int a;
    int c;
    cin >> a >> c;
    
    int b_square = c * c - a * a;
    cout << b_square << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int a;  // 직각을 끼는 주어진 변의 길이
//     int c;  // 주어진 빗변의 길이
//     cin >> a >> c;  // cin과 >>로 표준 입력의 값을 순서대로 읽기
//
//     int b_square = c * c - a * a;  // 빗변 제곱에서 알려진 변의 제곱을 빼 나머지 변의 제곱 구하기
//     cout << b_square << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 피타고라스 정리의 b² = c² - a²를 계산
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:30:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_250132_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_2%EB%B2%88___%ED%94%BC%ED%83%80%EA%B3%A0%EB%9D%BC%EC%8A%A4%EC%9D%98_%EC%A0%95%EB%A6%AC/README.md)
