# 코딩 테스트 공부

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/118668) · Level 3 · C++

## 풀이

문제 풀이와 두 종류 공부를 능력 증가 행동으로 두고 목표 능력치까지만 상태를 유지해 최소 시간 갱신

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(int alp, int cop, vector<vector<int>> problems) {
    int goal_alp = 0, goal_cop = 0;
    for (const auto& p : problems) { goal_alp = max(goal_alp, p[0]); goal_cop = max(goal_cop, p[1]); }
    alp = min(alp, goal_alp); cop = min(cop, goal_cop);
    problems.push_back({0,0,1,0,1}); problems.push_back({0,0,0,1,1});
    const int INF = 1000000000; vector<vector<int>> dp(goal_alp + 1, vector<int>(goal_cop + 1, INF)); dp[alp][cop] = 0;
    for (int a = alp; a <= goal_alp; ++a) for (int c = cop; c <= goal_cop; ++c) if (dp[a][c] != INF) {
        for (const auto& p : problems) if (a >= p[0] && c >= p[1]) {
            int na = min(goal_alp, a + p[2]), nc = min(goal_cop, c + p[3]);
            dp[na][nc] = min(dp[na][nc], dp[a][c] + p[4]);
        }
    }
    return dp[goal_alp][goal_cop];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int alp, int cop, vector<vector<int>> problems) {  // 목표 알고력·코딩력을 얻는 최소 시간 계산
// int goal_alp = 0, goal_cop = 0;  // 모든 문제를 풀기 위한 두 능력의 목표치 구하기
// for (const auto& p : problems) { goal_alp = max(goal_alp, p[0]); goal_cop = max(goal_cop, p[1]); }  // 문제별 요구 능력의 최댓값 읽기
// alp = min(alp, goal_alp); cop = min(cop, goal_cop);  // 목표를 넘는 초기 능력은 목표 값으로 줄이기
// problems.push_back({0,0,1,0,1}); problems.push_back({0,0,0,1,1});  // 두 능력을 각각 한 시간 공부하는 행동 추가
// const int INF = 1000000000; vector<vector<int>> dp(goal_alp + 1, vector<int>(goal_cop + 1, INF)); dp[alp][cop] = 0;  // 능력 상태별 최소 공부 시간 저장
// for (int a = alp; a <= goal_alp; ++a) for (int c = cop; c <= goal_cop; ++c) if (dp[a][c] != INF) {  // 작은 능력 상태부터 도달 가능한 상태 처리
// for (const auto& p : problems) if (a >= p[0] && c >= p[1]) {  // 현재 풀 수 있는 문제와 공부 행동 고르기
// int na = min(goal_alp, a + p[2]), nc = min(goal_cop, c + p[3]);  // 보상 능력을 목표치까지만 반영
// dp[na][nc] = min(dp[na][nc], dp[a][c] + p[4]);  // 행동 시간을 더해 다음 상태의 최소 비용 갱신
// }  // 블록 끝
// }  // 블록 끝
// return dp[goal_alp][goal_cop];  // 모든 문제를 풀 능력에 도달하는 최소 시간 반환
// }  // 블록 끝

// 풀이 요약
// 문제 풀이와 두 종류 공부를 능력 증가 행동으로 두고 목표 능력치까지만 상태를 유지해 최소 시간 갱신
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/031_118668_%EC%BD%94%EB%94%A9_%ED%85%8C%EC%8A%A4%ED%8A%B8_%EA%B3%B5%EB%B6%80/README.md)
