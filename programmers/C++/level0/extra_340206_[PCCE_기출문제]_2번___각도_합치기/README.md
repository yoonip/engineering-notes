# [PCCE 기출문제] 2번 / 각도 합치기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340206) · Level 0 · C++

## 풀이

각도 합을 360으로 나눈 나머지는 0 이상 360 미만이며 원래 각도와 같은 방향을 나타냅니다

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>

using namespace std;

int main(void) {
    int angle1;
    int angle2;
    cin >> angle1 >> angle2;
    
    int sum_angle = (angle1 + angle2) % 360;
    cout << sum_angle << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int angle1;  // 입력 각도를 저장할 int 변수를 선언
//     int angle2;  // 입력 각도를 저장할 int 변수를 선언
//     cin >> angle1 >> angle2;  // 입력 연산자 >>로 표준 입력의 값을 변수에 저장
//
//     int sum_angle = (angle1 + angle2) % 360;  // 두 각도의 합을 360으로 나눈 나머지로 0 이상 360 미만의 각도를 구하기
//     cout << sum_angle << endl;  // 계산한 각도를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 각도 합을 360으로 나눈 나머지는 0 이상 360 미만이며 원래 각도와 같은 방향을 나타냅니다
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:48:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_340206_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_2%EB%B2%88___%EA%B0%81%EB%8F%84_%ED%95%A9%EC%B9%98%EA%B8%B0/README.md)
