# 최소직사각형

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86491) · Level 1 · C++

## 풀이

명함마다 긴 변을 가로로 놓도록 방향 통일. 긴 변들의 최댓값과 짧은 변들의 최댓값을 곱함.

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <unordered_map>
#include <sstream>
#include <cctype>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <queue>
#include <set>
#include <climits>
#include <iostream>
using namespace std;

int solution(vector<vector<int>> sizes) {
    int width = 0, height = 0;
    for (const auto& size : sizes) { width = max(width, max(size[0], size[1])); height = max(height, min(size[0], size[1])); }
    return width * height;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열 string 사용 준비
// #include <vector>  // 가변 길이 배열 vector 사용 준비
// #include <algorithm>  // 정렬·탐색·최솟값 등 표준 알고리즘 사용 준비
// #include <numeric>  // gcd·accumulate 등 수치 알고리즘 사용 준비
// #include <functional>  // 함수 래퍼와 greater 등 비교 함수 객체 사용 준비
// #include <unordered_set>  // 중복 없는 원소를 저장하는 해시 집합 사용 준비
// #include <unordered_map>  // 키로 값을 찾는 해시 맵 사용 준비
// #include <sstream>  // 문자열을 토큰으로 나눠 읽을 스트림 사용 준비
// #include <cctype>  // 숫자·대소문자 검사와 변환 함수 사용 준비
// #include <cstdlib>  // 정수 절댓값 등 표준 유틸리티 함수 사용 준비
// #include <cstdio>  // snprintf 등 형식 있는 입출력 함수 사용 준비
// #include <cmath>  // 제곱근 등 수학 함수 사용 준비
// #include <queue>  // FIFO 큐와 우선순위 큐 사용 준비
// #include <set>  // 중복 제거와 정렬을 함께 하는 집합 사용 준비
// #include <climits>  // 정수 범위 상수 사용 준비
// #include <iostream>  // cin·cout 표준 입출력 사용 준비
// using namespace std;  // 표준 이름의 std:: 접두사 생략
//
// int solution(vector<vector<int>> sizes) {  // 최소직사각형 풀이 함수 정의
//     int width = 0, height = 0;  // 필요한 가로 width와 세로 height를 0으로 시작
//     for (const auto& size : sizes) { width = max(width, max(size[0], size[1])); height = max(height, min(size[0], size[1])); }  // 각 명함의 긴 변으로 width, 짧은 변으로 height의 최댓값 갱신
//     return width * height;  // 모든 명함이 들어가는 지갑의 최소 넓이 반환
// }  // 함수 끝
//

// 풀이 요약
// 명함마다 긴 변을 가로로 놓도록 방향 통일. 긴 변들의 최댓값과 짧은 변들의 최댓값을 곱함.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_86491_%EC%B5%9C%EC%86%8C%EC%A7%81%EC%82%AC%EA%B0%81%ED%98%95/README.md)
