# 귤 고르기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/138476) · Level 2 · C++

## 풀이

크기별 귤의 개수를 센 뒤 개수가 많은 크기부터 골라 필요한 양 채우기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <unordered_map>
#include <vector>
using namespace std;

int solution(int k, vector<int> tangerine) {
    unordered_map<int, int> counts;
    for (int size : tangerine) ++counts[size];
    vector<int> frequencies;
    for (const auto& entry : counts) frequencies.push_back(entry.second);
    sort(frequencies.begin(), frequencies.end(), greater<int>());
    int kinds = 0;
    for (int count : frequencies) {
        ++kinds; k -= count;
        if (k <= 0) return kinds;
    }
    return kinds;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int k, vector<int> tangerine) {  // 개수가 많은 귤 크기부터 골라 종류 수 줄이기
// unordered_map<int, int> counts;  // 크기별 귤의 개수를 해시 맵으로 세기
// for (int size : tangerine) ++counts[size];  // 같은 크기의 빈도를 증가시키기
// vector<int> frequencies;  // 크기별 개수만 별도 배열로 모으기
// for (const auto& entry : counts) frequencies.push_back(entry.second);  // 각 크기의 빈도를 배열에 넣기
// sort(frequencies.begin(), frequencies.end(), greater<int>());  // 많이 있는 크기부터 선택하도록 정렬
// int kinds = 0;  // 선택한 크기 종류 수 초기화
// for (int count : frequencies) {  // 빈도가 큰 크기부터 고르기
// ++kinds; k -= count;  // 종류 수를 늘리고 필요한 귤 수에서 해당 개수 빼기
// if (k <= 0) return kinds;  // 필요한 양을 채우면 최소 종류 수 반환
// }  // 블록 끝
// return kinds;  // 모든 귤을 선택한 경우의 종류 수 반환
// }  // 블록 끝

// 풀이 요약
// 크기별 귤의 개수를 센 뒤 개수가 많은 크기부터 골라 필요한 양 채우기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/035_138476_%EA%B7%A4_%EA%B3%A0%EB%A5%B4%EA%B8%B0/README.md)
