# 연속된 수의 합

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120923) · Level 0 · C++

## 풀이

연속된 수를 시작값+x로 표현하고 0부터 num-1까지의 합을 빼 시작값을 역산

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

vector<int> solution(int num, int total) {
    int first = (2 * total / num - num + 1) / 2;
    vector<int> answer(num);
    iota(answer.begin(), answer.end(), first);
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
// vector<int> solution(int num, int total) {  // 연속된 수의 합 풀이 시작
//     int first = (2 * total / num - num + 1) / 2;  // 연속된 num개 정수의 합이 total이 되는 첫 정수
//     vector<int> answer(num);  // 연속 정수 num개를 담을 배열
//     iota(answer.begin(), answer.end(), first);  // 구한 첫 정수부터 1씩 늘려 배열 채우기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 연속된 수를 시작값+x로 표현하고 0부터 num-1까지의 합을 빼 시작값을 역산
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120923_%EC%97%B0%EC%86%8D%EB%90%9C_%EC%88%98%EC%9D%98_%ED%95%A9/README.md)
