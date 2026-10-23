# 상담원 인원

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/214288) · Level 3 · C++

## 풀이

유형과 상담원 수별 대기 시간을 최소 힙으로 계산하고 총인원 배분을 동적 계획법으로 최적화

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <functional>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

int solution(int k, int n, vector<vector<int>> reqs) {
    vector<vector<pair<int, int>>> groups(k);
    for (const auto& request : reqs) groups[request[2] - 1].push_back({request[0], request[1]});
    int limit = n - k + 1; const int INF = 1000000000;
    vector<int> dp(n + 1, INF); dp[0] = 0;
    for (const auto& requests : groups) {
        vector<int> waiting(limit + 1, 0);
        for (int staff = 1; staff <= limit; ++staff) {
            priority_queue<int, vector<int>, greater<int>> heap; for (int i = 0; i < staff; ++i) heap.push(0);
            for (auto [start, duration] : requests) { int begin = max(start, heap.top()); heap.pop(); waiting[staff] += begin - start; heap.push(begin + duration); }
        }
        vector<int> next(n + 1, INF);
        for (int used = 0; used <= n; ++used) if (dp[used] != INF) for (int staff = 1; staff <= min(limit, n - used); ++staff) next[used + staff] = min(next[used + staff], dp[used] + waiting[staff]);
        dp = move(next);
    }
    return dp[n];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <queue>  // BFS 큐와 우선순위 큐
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int k, int n, vector<vector<int>> reqs) {  // 상담 유형별 인원 배분으로 총대기 시간 최소화
// vector<vector<pair<int, int>>> groups(k);  // 상담 유형별 요청의 시작과 소요 시간 저장
// for (const auto& request : reqs) groups[request[2] - 1].push_back({request[0], request[1]});  // 요청을 유형에 따라 분류
// int limit = n - k + 1; const int INF = 1000000000;  // 다른 유형에 한 명씩 배치한 뒤 가능한 최대 인원 구하기
// vector<int> dp(n + 1, INF); dp[0] = 0;  // 처리한 유형에 배치한 총인원별 최소 대기 시간 저장
// for (const auto& requests : groups) {  // 각 상담 유형의 인원 수 정하기
// vector<int> waiting(limit + 1, 0);  // 해당 유형의 인원 수별 총 대기 시간 저장
// for (int staff = 1; staff <= limit; ++staff) {  // 가능한 상담원 수를 모두 시뮬레이션
// priority_queue<int, vector<int>, greater<int>> heap; for (int i = 0; i < staff; ++i) heap.push(0);  // 상담원별 다음 가능 시각을 최소 힙으로 관리
// for (auto [start, duration] : requests) { int begin = max(start, heap.top()); heap.pop(); waiting[staff] += begin - start; heap.push(begin + duration); }  // 가장 빨리 비는 상담원에 요청을 배정하고 대기 시간을 더하기
// }  // 블록 끝
// vector<int> next(n + 1, INF);  // 새 유형까지 배치한 상태 초기화
// for (int used = 0; used <= n; ++used) if (dp[used] != INF) for (int staff = 1; staff <= min(limit, n - used); ++staff) next[used + staff] = min(next[used + staff], dp[used] + waiting[staff]);  // 현재 유형의 인원을 선택해 총 대기 시간 최소화
// dp = move(next);  // 새 유형까지의 최적 비용 적용
// }  // 블록 끝
// return dp[n];  // 모든 상담원을 배치했을 때의 최소 총 대기 시간 반환
// }  // 블록 끝

// 풀이 요약
// 유형과 상담원 수별 대기 시간을 최소 힙으로 계산하고 총인원 배분을 동적 계획법으로 최적화
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/016_214288_%EC%83%81%EB%8B%B4%EC%9B%90_%EC%9D%B8%EC%9B%90/README.md)
