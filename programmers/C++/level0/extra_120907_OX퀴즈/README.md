# OX퀴즈

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120907) · Level 0 · C++

## 풀이

등식을 다섯 항목으로 나누어 왼쪽 계산값과 오른쪽 숫자를 비교

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <sstream>
#include <climits>
#include <cctype>
#include <iostream>
#include <functional>

using namespace std;

vector<string> solution(vector<string> quiz) {
    vector<string> answer;
    for (const string& expression : quiz) {
        istringstream input(expression);
        int a, b, result;
        char operation, equal;
        input >> a >> operation >> b >> equal >> result;
        answer.push_back((operation == '+' ? a + b : a - b) == result ? "O" : "X");
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <cmath>  // 제곱근 등 수학 함수
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <climits>  // INT_MIN·INT_MAX 등 정수 범위 상수
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <iostream>  // cin·cout 표준 입출력
// #include <functional>  // greater·multiplies 등 함수 객체
//
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// vector<string> solution(vector<string> quiz) {  // OX퀴즈 풀이 시작
//     vector<string> answer;  // 각 등식이 맞는지 O·X로 기록
//     for (const string& expression : quiz) {  // 각 등식의 왼쪽 계산과 오른쪽 답을 비교
//         istringstream input(expression);  // expression를 공백 단위로 읽을 스트림 input
//         int a, b, result;  // a·b는 피연산자, result는 등식 오른쪽의 값
//         char operation, equal;  // 연산자와 등호를 읽어둘 문자 변수
//         input >> a >> operation >> b >> equal >> result;  // 두 피연산자·연산 기호·등호·제시된 답을 분리해 읽기
//         answer.push_back((operation == '+' ? a + b : a - b) == result ? "O" : "X");  // 왼쪽 계산값이 result와 같으면 O, 다르면 X 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 등식을 다섯 항목으로 나누어 왼쪽 계산값과 오른쪽 숫자를 비교
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:36:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120907_OX%ED%80%B4%EC%A6%88/README.md)
