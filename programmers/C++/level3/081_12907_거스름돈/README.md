# 거스름돈

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12907) · Level 3 · C++

## 풀이

동전 종류를 하나씩 추가하며 각 금액을 만드는 조합 수를 누적해 동전 사용 순서의 중복을 막기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(int n, vector<int> money) {
    vector<int> dp(n + 1,0); dp[0] = 1; const int MOD = 1000000007;
    for (int coin : money) for (int amount = coin; amount <= n; ++amount) dp[amount] = (dp[amount] + dp[amount - coin]) % MOD;
    return dp[n];
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<int> money) {  // 동전 종류를 하나씩 추가해 금액별 조합 수 계산
// vector<int> dp(n + 1,0); dp[0] = 1; const int MOD = 1000000007;  // 금액 0을 만드는 빈 조합 하나에서 시작
// for (int coin : money) for (int amount = coin; amount <= n; ++amount) dp[amount] = (dp[amount] + dp[amount - coin]) % MOD;  // 동전 종류를 바깥 반복으로 두어 순서 중복 없이 조합 수를 더하기
// return dp[n];  // n원을 만드는 방법 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 동전 종류를 하나씩 추가하며 각 금액을 만드는 조합 수를 누적해 동전 사용 순서의 중복을 막기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:49:04
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/081_12907_%EA%B1%B0%EC%8A%A4%EB%A6%84%EB%8F%88/README.md)
