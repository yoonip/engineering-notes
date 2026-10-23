# 정수 찾기

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181840) · Level 0 · C++

## 풀이

표준 알고리즘 find로 n을 찾기. 반환한 반복자가 num_list.end()와 다르면 1, 같으면 0을 반환

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

int solution(vector<int> num_list, int n) {
    return find(num_list.begin(), num_list.end(), n) != num_list.end();
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
// int solution(vector<int> num_list, int n) {  // 정수 찾기 풀이 시작
//     return find(num_list.begin(), num_list.end(), n) != num_list.end();  // find로 n을 검색하고 반환 반복자가 end와 다르면 참인 1, 끝까지 없으면 거짓인 0을 반환
// }  // 블록 끝

// 풀이 요약
// 표준 알고리즘 find로 n을 찾기. 반환한 반복자가 num_list.end()와 다르면 1, 같으면 0을 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:21:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181840_%EC%A0%95%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
