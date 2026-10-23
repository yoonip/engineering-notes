# 최빈값 구하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120812) · Level 0 · C++

## 풀이

등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인

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

int solution(vector<int> array) {
    int counts[1000] = {}, best = 0, answer = -1;
    for (int value : array) ++counts[value];
    for (int value = 0; value < 1000; ++value) {
        if (counts[value] > best) { best = counts[value]; answer = value; }
        else if (counts[value] == best) answer = -1;
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
// int solution(vector<int> array) {  // 최빈값 구하기 풀이 시작
//     int counts[1000] = {}, best = 0, answer = -1;  // 값별 등장 횟수, 최대 빈도, 유일한 최빈값 후보
//     for (int value : array) ++counts[value];  // 각 값의 등장 횟수 집계
//     for (int value = 0; value < 1000; ++value) {  // 값별 빈도를 비교해 유일한 최빈값 찾기
//         if (counts[value] > best) { best = counts[value]; answer = value; }  // 더 큰 빈도를 찾으면 최댓값과 후보를 함께 교체
//         else if (counts[value] == best) answer = -1;  // 최대 빈도가 같으면 아직 유일하지 않으니 -1
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120812_%EC%B5%9C%EB%B9%88%EA%B0%92_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
