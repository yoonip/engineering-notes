# 스티커 모으기(2)

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12971) · Level 3 · C++

## 풀이

첫 스티커를 제외하거나 마지막 스티커를 제외하는 두 일자 구간에서 인접 선택 없는 최대 합 구하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<int> sticker) {
    int n = (int)sticker.size(); if (n == 1) return sticker[0];
    auto linear = [&](int start, int end) {
        int two_before = 0, one_before = 0;
        for (int i = start; i < end; ++i) { int current = max(one_before, two_before + sticker[i]); two_before = one_before; one_before = current; }
        return one_before;
    };
    return max(linear(0,n - 1), linear(1,n));
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> sticker) {  // 원형의 양 끝 중 하나를 제외한 최대 합 비교
// int n = (int)sticker.size(); if (n == 1) return sticker[0];  // 스티커 하나이면 그 값을 바로 선택
// auto linear = [&](int start, int end) {  // 인접 선택을 금지한 일자 구간의 최대 합 구하기
// int two_before = 0, one_before = 0;  // 두 칸 전과 한 칸 전의 최적 합 초기화
// for (int i = start; i < end; ++i) { int current = max(one_before, two_before + sticker[i]); two_before = one_before; one_before = current; }  // 현재 스티커를 고르거나 건너뛰는 두 경우 비교
// return one_before;  // 구간의 최대 합 반환
// };  // 블록 끝
// return max(linear(0,n - 1), linear(1,n));  // 첫 스티커 또는 마지막 스티커를 제외한 두 경우 비교
// }  // 블록 끝

// 풀이 요약
// 첫 스티커를 제외하거나 마지막 스티커를 제외하는 두 일자 구간에서 인접 선택 없는 최대 합 구하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/076_12971_%EC%8A%A4%ED%8B%B0%EC%BB%A4_%EB%AA%A8%EC%9C%BC%EA%B8%B0%282%29/README.md)
