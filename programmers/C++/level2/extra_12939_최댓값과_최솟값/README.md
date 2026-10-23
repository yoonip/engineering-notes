# 최댓값과 최솟값

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12939) · Level 2 · C++

## 풀이

문자열에서 모든 정수를 읽어 최솟값과 최댓값을 구한 뒤 공백으로 연결

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <climits>
#include <sstream>
#include <string>
using namespace std;

string solution(string s) {
    istringstream input(s); int value, lowest = INT_MAX, highest = INT_MIN;
    while (input >> value) { lowest = min(lowest, value); highest = max(highest, value); }
    return to_string(lowest) + " " + to_string(highest);
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <climits>  // 정수 자료형의 최솟값·최댓값
// #include <sstream>  // 문자열에서 공백 단위로 값을 읽는 스트림
// #include <string>  // 문자열을 담는 string
// using namespace std;  // std:: 접두사 생략
// string solution(string s) {  // 공백으로 구분된 정수의 최솟값·최댓값 찾기
// istringstream input(s); int value, lowest = INT_MAX, highest = INT_MIN;  // 정수 입력 스트림과 최솟값 및 최댓값 초기화
// while (input >> value) { lowest = min(lowest, value); highest = max(highest, value); }  // 문자열의 모든 정수를 읽어 두 경계 갱신
// return to_string(lowest) + " " + to_string(highest);  // 최솟값과 최댓값을 공백으로 연결해 반환
// }  // 블록 끝

// 풀이 요약
// 문자열에서 모든 정수를 읽어 최솟값과 최댓값을 구한 뒤 공백으로 연결
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:37:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/extra_12939_%EC%B5%9C%EB%8C%93%EA%B0%92%EA%B3%BC_%EC%B5%9C%EC%86%9F%EA%B0%92/README.md)
