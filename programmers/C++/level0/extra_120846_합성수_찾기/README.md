# 합성수 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120846) · Level 0 · C++

## 풀이

4부터 n까지 각 수에 대해 제곱근 이하의 약수를 찾기. 하나라도 있으면 합성수로 한 번만 세기

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

int solution(int n) {
    int count = 0;
    for (int value = 4; value <= n; ++value)
        for (int d = 2; d <= value / d; ++d)
            if (value % d == 0) { ++count; break; }
    return count;
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
// int solution(int n) {  // 합성수 찾기 풀이 시작
//     int count = 0;  // 1과 자기 자신 외의 약수를 찾은 합성수 개수
//     for (int value = 4; value <= n; ++value)  // 가장 작은 합성수 4부터 n까지 확인
//         for (int d = 2; d <= value / d; ++d)  // 제곱근 이하에서 1이 아닌 약수 찾기
//             if (value % d == 0) { ++count; break; }  // if 조건이 참이면 결과를 반영하고 break로 가장 안쪽 반복문을 끝
//     return count;  // 범위 안의 합성수 총개수
// }  // 블록 끝

// 풀이 요약
// 4부터 n까지 각 수에 대해 제곱근 이하의 약수를 찾기. 하나라도 있으면 합성수로 한 번만 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120846_%ED%95%A9%EC%84%B1%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
