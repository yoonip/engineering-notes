# 머쓱이보다 키 큰 사람

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120585) · Level 0 · C++

## 풀이

같은 키는 제외하고 기준 키보다 큰 사람만 세기

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

int solution(vector<int> array, int height) {
    return count_if(array.begin(), array.end(), [height](int value) { return value > height; });
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
// int solution(vector<int> array, int height) {  // 머쓱이보다 키 큰 사람 풀이 시작
//     return count_if(array.begin(), array.end(), [height](int value) { return value > height; });  // 기준 키보다 큰 원소만 세어 인원 수 반환
// }  // 블록 끝

// 풀이 요약
// 같은 키는 제외하고 기준 키보다 큰 사람만 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120585_%EB%A8%B8%EC%93%B1%EC%9D%B4%EB%B3%B4%EB%8B%A4_%ED%82%A4_%ED%81%B0_%EC%82%AC%EB%9E%8C/README.md)
