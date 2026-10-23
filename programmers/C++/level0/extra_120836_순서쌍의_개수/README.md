# 순서쌍의 개수

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120836) · Level 0 · C++

## 풀이

1부터 제곱근 이하까지 n의 약수를 검사. i와 n / i가 다르면 순서를 바꾼 두 쌍을 세고, 같으면 제곱근에 해당하는 한 쌍만 세기

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
    for (int i = 1; i <= n / i; ++i)
        if (n % i == 0) count += i == n / i ? 1 : 2;
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
// int solution(int n) {  // 순서쌍의 개수 풀이 시작
//     int count = 0;  // int 변수 count를 0으로 초기화하여 찾은 순서쌍의 수를 누적
//     for (int i = 1; i <= n / i; ++i)  // i를 1부터 n의 제곱근 이하까지만 검사. i * i 대신 i <= n / i로 비교하여 큰 제곱의 계산을 피
//         if (n % i == 0) count += i == n / i ? 1 : 2;  // 나머지가 0인 약수 i에 대해, i와 n / i가 같으면 한 쌍을 더하고 다르면 순서를 바꾼 두 쌍을 더하기
//     return count;  // 검사한 약수 쌍으로 센 순서쌍의 총수 count를 반환
// }  // 블록 끝

// 풀이 요약
// 1부터 제곱근 이하까지 n의 약수를 검사. i와 n / i가 다르면 순서를 바꾼 두 쌍을 세고, 같으면 제곱근에 해당하는 한 쌍만 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:32:35
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120836_%EC%88%9C%EC%84%9C%EC%8C%8D%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
