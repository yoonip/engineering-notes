# 선입 선출 스케줄링

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12920) · Level 3 · C++

## 풀이

누적 작업 배정 수로 n번째 작업이 시작되는 시각을 이분 탐색하고 그 시각에 비는 코어를 번호순으로 확인

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(int n, vector<int> cores) {
    int count = (int)cores.size(); if (n <= count) return n;
    long long left = 1, right = 1LL * *min_element(cores.begin(), cores.end()) * (n - count);
    while (left < right) {
        long long middle = left + (right - left) / 2, assigned = count;
        for (int core : cores) assigned += middle / core;
        if (assigned >= n) right = middle; else left = middle + 1;
    }
    long long time = left, remaining = n - count;
    for (int core : cores) remaining -= (time - 1) / core;
    for (int i = 0; i < count; ++i) if (time % cores[i] == 0 && --remaining == 0) return i + 1;
    return 0;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<int> cores) {  // n번째 작업의 시작 시각과 담당 코어 찾기
// int count = (int)cores.size(); if (n <= count) return n;  // 시각 0에 각 코어에 배정되는 작업은 번호가 바로 정해짐
// long long left = 1, right = 1LL * *min_element(cores.begin(), cores.end()) * (n - count);  // n번째 작업이 배정되는 시각의 범위 구하기
// while (left < right) {  // 누적 배정 수가 n 이상인 첫 시각 찾기
// long long middle = left + (right - left) / 2, assigned = count;  // 시각 후보와 처음 배정한 작업 수 초기화
// for (int core : cores) assigned += middle / core;  // 각 코어가 추가로 시작할 작업 수를 더하기
// if (assigned >= n) right = middle; else left = middle + 1;  // 누적 배정 수에 따라 시간 범위 줄이기
// }  // 블록 끝
// long long time = left, remaining = n - count;  // 경계 시각에 남은 작업 순번 계산
// for (int core : cores) remaining -= (time - 1) / core;  // 직전 시각까지 이미 배정한 작업 수 빼기
// for (int i = 0; i < count; ++i) if (time % cores[i] == 0 && --remaining == 0) return i + 1;  // 경계 시각에 비는 코어를 번호순으로 배정하기
// return 0;  // 유효한 입력에서는 도달하지 않는 기본 반환
// }  // 블록 끝

// 풀이 요약
// 누적 작업 배정 수로 n번째 작업이 시작되는 시각을 이분 탐색하고 그 시각에 비는 코어를 번호순으로 확인
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/080_12920_%EC%84%A0%EC%9E%85_%EC%84%A0%EC%B6%9C_%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/README.md)
