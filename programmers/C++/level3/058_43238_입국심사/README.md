# 입국심사

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/43238) · Level 3 · C++

## 풀이

전체 시간을 이분 탐색하고 각 심사관의 처리 인원 합이 n 이상인지 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

long long solution(int n, vector<int> times) {
    long long left = 0, right = 1LL * *min_element(times.begin(), times.end()) * n;
    while (left < right) {
        long long middle = left + (right - left) / 2, completed = 0;
        for (int time : times) { completed += middle / time; if (completed >= n) break; }
        if (completed >= n) right = middle; else left = middle + 1;
    }
    return left;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// long long solution(int n, vector<int> times) {  // 주어진 시간의 심사 인원으로 최소 완료 시각 찾기
// long long left = 0, right = 1LL * *min_element(times.begin(), times.end()) * n;  // 가장 빠른 심사관이 모두 처리할 시간을 상한으로 두기
// while (left < right) {  // n명을 심사할 수 있는 최소 시간을 이분 탐색
// long long middle = left + (right - left) / 2, completed = 0;  // 시간 후보와 완료 인원 수 초기화
// for (int time : times) { completed += middle / time; if (completed >= n) break; }  // 심사관별 완료 인원을 더하고 충분하면 멈추기
// if (completed >= n) right = middle; else left = middle + 1;  // 가능 여부에 따라 시간 범위 줄이기
// }  // 블록 끝
// return left;  // 최소 전체 심사 시간 반환
// }  // 블록 끝

// 풀이 요약
// 전체 시간을 이분 탐색하고 각 심사관의 처리 인원 합이 n 이상인지 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:43:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/058_43238_%EC%9E%85%EA%B5%AD%EC%8B%AC%EC%82%AC/README.md)
