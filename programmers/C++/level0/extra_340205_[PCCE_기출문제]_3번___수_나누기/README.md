# [PCCE 기출문제] 3번 / 수 나누기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340205) · Level 0 · C++

## 풀이

100으로 나눈 나머지로 마지막 두 자리를 얻어 더하고, 100으로 나누어 자릿수를 줄이는 작업을 반복

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 문제. 사이트에는 정해진 부분만 제출했고, 이 파일은 전체 코드에 메모를 붙인 보관용.

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <iostream>

using namespace std;

int main(void) {
    int number;
    cin >> number;
    
    int answer = 0;
    
    while(number > 0){
        answer += number % 100;
        number /= 100;
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
//     int number;  // 두 자리씩 나눌 입력 정수를 저장할 변수를 선언
//     cin >> number;  // 입력 연산자 >>로 표준 입력의 값을 변수에 저장
//
//     int answer = 0;  // 잘라낸 수들의 합계를 0으로 초기화
//
//     while(number > 0){  // while문으로 처리할 자릿수가 남아 있는 동안 반복
//         answer += number % 100;  // %로 얻은 마지막 두 자리 값을 +=로 합계에 더하기
//         number /= 100;  // 정수 나눗셈으로 이미 더한 마지막 두 자리를 제거
//     }  // 블록 끝
//     cout << answer << endl;  // 두 자리씩 잘라 더한 합계와 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 100으로 나눈 나머지로 마지막 두 자리를 얻어 더하고, 100으로 나누어 자릿수를 줄이는 작업을 반복
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:48:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_340205_%5BPCCE_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_3%EB%B2%88___%EC%88%98_%EB%82%98%EB%88%84%EA%B8%B0/README.md)
