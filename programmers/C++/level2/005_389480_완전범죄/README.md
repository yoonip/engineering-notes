# 완전범죄

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389480) · Level 2 · C++

## 풀이

B의 흔적 수를 상태로 두고 각 물건을 A 또는 B에게 배정할 때 가능한 최소 A 흔적 갱신

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<vector<int>> info, int n, int m) {
    vector<int> dp(m, n);
    dp[0] = 0;
    for (const auto& trace : info) {
        vector<int> next(m, n);
        for (int b = 0; b < m; ++b) {
            if (dp[b] == n) continue;
            if (dp[b] + trace[0] < n) next[b] = min(next[b], dp[b] + trace[0]);
            if (b + trace[1] < m) next[b + trace[1]] = min(next[b + trace[1]], dp[b]);
        }
        dp = move(next);
    }
    int answer = *min_element(dp.begin(), dp.end());
    return answer < n ? answer : -1;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> info, int n, int m) {  // B 흔적 제한을 지키며 A 흔적 최소화
// vector<int> dp(m, n);  // B의 흔적별 최소 A 흔적을 저장하고 불가능 상태는 n으로 두기
// dp[0] = 0;  // 아무 물건도 처리하지 않은 초기 상태
// for (const auto& trace : info) {  // 각 물건을 두 사람 중 한 명에게 배정하기
// vector<int> next(m, n);  // 현재 물건까지 반영할 새 상태 초기화
// for (int b = 0; b < m; ++b) {  // 기존 B 흔적 수를 순회
// if (dp[b] == n) continue;  // 도달할 수 없는 상태는 건너뛰기
// if (dp[b] + trace[0] < n) next[b] = min(next[b], dp[b] + trace[0]);  // A에게 배정해 제한 미만이면 최소 흔적 갱신
// if (b + trace[1] < m) next[b + trace[1]] = min(next[b + trace[1]], dp[b]);  // B에게 배정해 제한 미만이면 상태 갱신
// }  // 블록 끝
// dp = move(next);  // 새 상태를 다음 물건의 기준으로 사용
// }  // 블록 끝
// int answer = *min_element(dp.begin(), dp.end());  // 가능한 모든 B 흔적 중 최소 A 흔적 구하기
// return answer < n ? answer : -1;  // 가능한 배정이 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// B의 흔적 수를 상태로 두고 각 물건을 A 또는 B에게 배정할 때 가능한 최소 A 흔적 갱신
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:25:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/005_389480_%EC%99%84%EC%A0%84%EB%B2%94%EC%A3%84/README.md)
