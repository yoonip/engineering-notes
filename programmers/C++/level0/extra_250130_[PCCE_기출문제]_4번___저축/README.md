# [PCCE 기출문제] 4번 / 저축

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250130) · Level 0 · C++

## 풀이

첫 달의 금액으로 시작. 70만 원 미만일 때 before를 더하고 그 이후에는 after를 더해 100만 원에 도달한 개월 수를 세기

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>

using namespace std;

int main(void) {
    int start;
    int before;
    int after;
    cin >> start >> before >> after;

    int money = start;
    int month = 1;

    while (money < 70) {
        money += before;
        month++;
    }
    while (money < 100) {
        money += after;
        month++;
    }
    cout << month << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int start;  // 첫 달에 모은 금액
//     int before;  // 70만 원에 도달하기 전 매달 저축할 금액
//     int after;  // 70만 원부터 매달 저축할 금액
//     cin >> start >> before >> after;  // cin과 >>로 표준 입력의 값을 순서대로 읽기
//
//     int money = start;  // 첫 달의 저축액을 현재 잔액으로 설정
//     int month = 1;  // 첫 달 저축이 이미 반영되어 있으니 1개월
//
//     while (money < 70) {  // 잔액이 70만 원보다 작을 때의 저축
//         money += before;  // 초기 월 저축액을 잔액에 추가
//         month++;  // 저축한 달 하나 추가
//     }  // 블록 끝
//     while (money < 100) {  // 월 저축액을 바꾼 뒤 100만 원까지 모으기
//         money += after;  // 변경된 월 저축액을 잔액에 추가
//         month++;  // 저축한 달 하나 추가
//     }  // 블록 끝
//     cout << month << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 첫 달의 금액으로 시작. 70만 원 미만일 때 before를 더하고 그 이후에는 after를 더해 100만 원에 도달한 개월 수를 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:15
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_250130_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_4%EB%B2%88___%EC%A0%80%EC%B6%95/README.md)
