# 2의 영역

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181894) · Level 0 · C++

## 풀이

모든 2를 포함하려면 첫 2에서 마지막 2까지의 구간이 필요

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

vector<int> solution(vector<int> arr) {
    auto first = find(arr.begin(), arr.end(), 2);
    if (first == arr.end()) return {-1};
    auto last = find(arr.rbegin(), arr.rend(), 2).base();
    return vector<int>(first, last);
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
// vector<int> solution(vector<int> arr) {  // 2의 영역 풀이 시작
//     auto first = find(arr.begin(), arr.end(), 2);  // find로 처음 등장한 2의 반복자 위치를 찾기
//     if (first == arr.end()) return {-1};  // 2가 하나도 없으면 실패 표시 -1만 담아 반환
//     auto last = find(arr.rbegin(), arr.rend(), 2).base();  // 역방향 find와 base로 마지막 2 바로 다음의 반복자를 구하기
//     return vector<int>(first, last);  // 두 반복자가 가리키는 반열린 구간을 복사해 새 vector로 반환
// }  // 블록 끝

// 풀이 요약
// 모든 2를 포함하려면 첫 2에서 마지막 2까지의 구간이 필요
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:04:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181894_2%EC%9D%98_%EC%98%81%EC%97%AD/README.md)
