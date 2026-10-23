# 숫자 짝꿍

[레벨 1 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131128) · Level 1 · C++

## 풀이

두 문자열에서 숫자별 등장 횟수를 셈. 공통으로 쓸 수 있는 횟수만큼 9부터 붙여 가장 큰 수 생성.

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

string solution(string X, string Y) {
    int x[10] = {0}, y[10] = {0};
    for (char c : X) ++x[c - '0']; for (char c : Y) ++y[c - '0'];
    string answer;
    for (int digit = 9; digit >= 0; --digit) answer.append(min(x[digit], y[digit]), char('0' + digit));
    if (answer.empty()) return "-1";
    if (answer[0] == '0') return "0";
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
// string solution(string X, string Y) {  // 숫자 짝꿍 풀이 함수 정의
//     int x[10] = {0}, y[10] = {0};  // X와 Y의 숫자별 등장 횟수 배열을 각각 0으로 초기화
//     for (char c : X) ++x[c - '0']; for (char c : Y) ++y[c - '0'];  // 각 문자를 0~9 인덱스로 바꿔 두 문자열의 숫자 빈도 기록
//     string answer;  // 공통 숫자로 만들 결과 문자열 준비
//     for (int digit = 9; digit >= 0; --digit) answer.append(min(x[digit], y[digit]), char('0' + digit));  // 9부터 0까지 두 빈도의 최솟값만큼 문자를 붙여 최댓값 생성
//     if (answer.empty()) return "-1";  // 공통 숫자가 없으면 -1 반환
//     if (answer[0] == '0') return "0";  // 가장 큰 숫자가 0이면 전부 0이므로 한 글자 0만 반환
//     return answer;  // 내림차순으로 배치한 공통 숫자 문자열 반환
// }  // 함수 끝
//

// 풀이 요약
// 두 문자열에서 숫자별 등장 횟수를 셈. 공통으로 쓸 수 있는 횟수만큼 9부터 붙여 가장 큰 수 생성.
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:11:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_131128_%EC%88%AB%EC%9E%90_%EC%A7%9D%EA%BF%8D/README.md)
