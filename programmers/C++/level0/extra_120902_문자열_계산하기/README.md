# 문자열 계산하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120902) · Level 0 · C++

## 풀이

연산 기호와 그 다음 숫자를 한 쌍씩 처리하여 앞에서부터 계산

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

int solution(string my_string) {
    istringstream input(my_string);
    int answer, value;
    char operation;
    input >> answer;
    while (input >> operation >> value) answer += operation == '+' ? value : -value;
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
// int solution(string my_string) {  // 문자열 계산하기 풀이 시작
//     istringstream input(my_string);  // my_string를 공백 단위로 읽을 스트림 input
//     int answer, value;  // answer를 저장할 변수 · value를 저장할 변수
//     char operation;  // operation를 저장할 변수
//     input >> answer;  // 첫 숫자를 읽어 계산의 시작값으로 설정
//     while (input >> operation >> value) answer += operation == '+' ? value : -value;  // while은 스트림에서 다음 토큰·연산을 읽을 수 있는 동안 반복
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 연산 기호와 그 다음 숫자를 한 쌍씩 처리하여 앞에서부터 계산
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:39:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120902_%EB%AC%B8%EC%9E%90%EC%97%B4_%EA%B3%84%EC%82%B0%ED%95%98%EA%B8%B0/README.md)
