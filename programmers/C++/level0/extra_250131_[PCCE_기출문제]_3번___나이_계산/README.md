# [PCCE 기출문제] 3번 / 나이 계산

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/250131) · Level 0 · C++

## 풀이

2030에서 출생 연도를 빼서 연 나이를 구하기. 한국식 나이는 그 값에 1을 더하기

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>

using namespace std;

int main(void) {
    int year, answer;
    string age_type;
    cin >> year >> age_type;

    if (age_type == "Korea") {
        answer = 2030 - year + 1;
    }
    else if (age_type == "Year") {
        answer = 2030 - year;
    }

    cout << answer << endl;
    return 0;
}

// 전체 코드 줄별 설명
// #include <iostream>  // cin·cout 표준 입출력
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     int year, answer;  // 출생 연도와 계산한 나이
//     string age_type;  // 한국식 나이인지 연 나이인지 구분할 문자열
//     cin >> year >> age_type;  // cin과 >>로 표준 입력의 값을 순서대로 읽기
//
//     if (age_type == "Korea") {  // age_type == "Korea"이면 이 분기에서 처리
//         answer = 2030 - year + 1;  // 태어난 해를 한 살로 세는 한국식 나이
//     }  // 블록 끝
//     else if (age_type == "Year") {  // 출생 연도 차이로 세는 연 나이
//         answer = 2030 - year;  // 2030년과 출생 연도의 차이
//     }  // 블록 끝
//
//     cout << answer << endl;  // cout과 <<로 계산 결과를 출력하고 endl로 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 2030에서 출생 연도를 빼서 연 나이를 구하기. 한국식 나이는 그 값에 1을 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_250131_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_3%EB%B2%88___%EB%82%98%EC%9D%B4_%EA%B3%84%EC%82%B0/README.md)
