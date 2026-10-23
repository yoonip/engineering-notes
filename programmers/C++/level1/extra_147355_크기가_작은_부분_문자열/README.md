# 크기가 작은 부분 문자열

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/147355) · Level 1 · C++

## 풀이

p와 같은 길이의 t 부분 문자열을 검사. 길이가 같은 숫자 문자열은 사전순 비교와 수치 비교가 같으므로 정수 변환 없이 비교.

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

int solution(string t, string p) {
    int answer = 0;
    for (size_t i = 0; i + p.size() <= t.size(); ++i) if (t.compare(i, p.size(), p) <= 0) ++answer;
    return answer;
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
// int solution(string t, string p) {  // 크기가 작은 부분 문자열 풀이 함수 정의
//     int answer = 0;  // 조건을 만족하는 부분 문자열 수를 0부터 셈
//     for (size_t i = 0; i + p.size() <= t.size(); ++i) if (t.compare(i, p.size(), p) <= 0) ++answer;  // p 길이만큼 자를 수 있는 모든 시작점에서 compare로 p 이하인지 확인해 개수 증가
//     return answer;  // 조건을 만족한 부분 문자열 수 반환
// }  // 함수 끝
//

// 풀이 요약
// p와 같은 길이의 t 부분 문자열을 검사. 길이가 같은 숫자 문자열은 사전순 비교와 수치 비교가 같으므로 정수 변환 없이 비교.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:08:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_147355_%ED%81%AC%EA%B8%B0%EA%B0%80_%EC%9E%91%EC%9D%80_%EB%B6%80%EB%B6%84_%EB%AC%B8%EC%9E%90%EC%97%B4/README.md)
