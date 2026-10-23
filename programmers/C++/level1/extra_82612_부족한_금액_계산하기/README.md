# 부족한 금액 계산하기

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/82612) · Level 1 · C++

## 풀이

이용료 합은 price × (1 + … + count). 등차수열 공식으로 합산하고 보유금보다 부족한 금액만 반환.

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

long long solution(int price, int money, int count) {
    return max(0LL, 1LL * price * count * (count + 1) / 2 - money);
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
// long long solution(int price, int money, int count) {  // 부족한 금액 계산하기 풀이 함수 정의
//     return max(0LL, 1LL * price * count * (count + 1) / 2 - money);  // 중간 곱의 오버플로를 피하려고 1LL로 long long 계산. 전체 이용료에서 보유금을 빼고 0과 비교해 부족분만 반환
// }  // 함수 끝
//

// 풀이 요약
// 이용료 합은 price × (1 + … + count). 등차수열 공식으로 합산하고 보유금보다 부족한 금액만 반환.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_82612_%EB%B6%80%EC%A1%B1%ED%95%9C_%EA%B8%88%EC%95%A1_%EA%B3%84%EC%82%B0%ED%95%98%EA%B8%B0/README.md)
