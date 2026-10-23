# 가까운 수

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120890) · Level 0 · C++

## 풀이

각 원소와 n의 절댓값 차이를 비교. 거리가 더 가까운 원소를 선택하고, 거리가 같으면 더 작은 원소를 선택

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

int solution(vector<int> array, int n) {
    int answer = array[0];
    for (int value : array)
        if (abs(value - n) < abs(answer - n) || (abs(value - n) == abs(answer - n) && value < answer)) answer = value;
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
// int solution(vector<int> array, int n) {  // 가까운 수 풀이 시작
//     int answer = array[0];  // 첫 원소 array[0]을 현재까지 가장 가까운 수 answer로 정하여 비교를 시작
//     for (int value : array)  // 범위 기반 for로 배열의 각 후보 원소를 value에 읽기
//         if (abs(value - n) < abs(answer - n) || (abs(value - n) == abs(answer - n) && value < answer)) answer = value;  // abs로 후보와 n의 거리, 현재 answer와 n의 거리를 비교. 후보의 거리가 더 작거나, 거리가 같으면서 후보 값이 더 작을 때만 answer를 교체
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 원소와 n의 절댓값 차이를 비교. 거리가 더 가까운 원소를 선택하고, 거리가 같으면 더 작은 원소를 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:28:06
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120890_%EA%B0%80%EA%B9%8C%EC%9A%B4_%EC%88%98/README.md)
