# 튜플

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/64065) · Level 2 · C++

## 풀이

튜플의 앞 원소일수록 더 많은 집합에 나타나는 성질을 이용해 원소별 등장 횟수를 내림차순 정렬

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(string s) {
    unordered_map<int, int> counts;
    int value = 0; bool reading = false;
    for (char c : s) {
        if (c >= '0' && c <= '9') { value = value * 10 + c - '0'; reading = true; }
        else if (reading) { ++counts[value]; value = 0; reading = false; }
    }
    vector<pair<int, int>> ranked;
    for (const auto& entry : counts) ranked.push_back({entry.second, entry.first});
    sort(ranked.rbegin(), ranked.rend());
    vector<int> answer;
    for (const auto& entry : ranked) answer.push_back(entry.second);
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(string s) {  // 작은 집합부터 새 원소를 찾아 튜플 복원
// unordered_map<int, int> counts;  // 각 원소가 집합들에 등장한 횟수 세기
// int value = 0; bool reading = false;  // 현재 정수 토큰과 읽는 중인지 여부 저장
// for (char c : s) {  // 문자열에서 정수 토큰만 추출
// if (c >= '0' && c <= '9') { value = value * 10 + c - '0'; reading = true; }  // 숫자를 이어 붙여 정수 만들기
// else if (reading) { ++counts[value]; value = 0; reading = false; }  // 구분자를 만나면 해당 원소의 등장 횟수 늘리기
// }  // 블록 끝
// vector<pair<int, int>> ranked;  // 등장 횟수와 원소를 정렬할 배열 만들기
// for (const auto& entry : counts) ranked.push_back({entry.second, entry.first});  // 빈도를 먼저 비교할 수 있도록 순서 바꾸기
// sort(ranked.rbegin(), ranked.rend());  // 자주 등장한 원소가 먼저 오게 정렬
// vector<int> answer;  // 원래 튜플의 순서 저장
// for (const auto& entry : ranked) answer.push_back(entry.second);  // 빈도순으로 원소 추가
// return answer;  // 복원한 튜플 반환
// }  // 블록 끝

// 풀이 요약
// 튜플의 앞 원소일수록 더 많은 집합에 나타나는 성질을 이용해 원소별 등장 횟수를 내림차순 정렬
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/063_64065_%ED%8A%9C%ED%94%8C/README.md)
