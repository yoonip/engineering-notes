# n보다 커질 때까지 더하기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181884) · Level 0 · C++

## 풀이

앞에서부터 더하되 합이 n과 같을 때는 계속하고, n보다 커진 순간의 합 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <functional>
#include <unordered_set>
#include <sstream>
#include <cctype>
#include <cstdlib>
using namespace std;

int solution(vector<int> numbers, int n) {
    int sum = 0;
    for (int value : numbers) { sum += value; if (sum > n) break; }
    return sum;
}

// 전체 코드 줄별 설명
// #include <string>  // 문자열을 다룰 string
// #include <vector>  // 길이를 늘릴 수 있는 vector
// #include <algorithm>  // 정렬·검색·뒤집기 알고리즘
// #include <numeric>  // accumulate·iota 등 수치 연산
// #include <functional>  // greater·multiplies 등 함수 객체
// #include <unordered_set>  // 중복을 거를 해시 집합
// #include <sstream>  // 문자열을 항목별로 읽을 스트림
// #include <cctype>  // 문자 검사와 대소문자 변환
// #include <cstdlib>  // 정수 변환과 절댓값 등 표준 함수
// using namespace std;  // 표준 라이브러리 이름의 std:: 생략
//
// int solution(vector<int> numbers, int n) {  // n보다 커질 때까지 더하기 풀이 시작
//     int sum = 0;  // 앞에서부터 더한 원소의 합
//     for (int value : numbers) { sum += value; if (sum > n) break; }  // 현재 원소까지 더한 뒤 합이 n을 초과하면 중단
//     return sum;  // 누적 합계 값을 반환하고 함수를 끝
// }  // 블록 끝

// 풀이 요약
// 앞에서부터 더하되 합이 n과 같을 때는 계속하고, n보다 커진 순간의 합 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:07:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181884_n%EB%B3%B4%EB%8B%A4_%EC%BB%A4%EC%A7%88_%EB%95%8C%EA%B9%8C%EC%A7%80_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
