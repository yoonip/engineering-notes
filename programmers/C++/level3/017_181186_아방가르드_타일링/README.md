# 아방가르드 타일링

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181186) · Level 3 · C++

## 풀이

작은 너비의 초기값에서 기본 및 특수 타일 배치의 점화식을 적용하고 중복된 여섯 칸 이전 항 빼기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(int n) {
    const long long MOD = 1000000007; vector<long long> dp(n + 4, 0);
    dp[0] = 1; dp[1] = 1; dp[2] = 3; dp[3] = 10;
    for (int width = 4; width <= n; ++width) {
        long long subtract = width >= 6 ? dp[width - 6] : 0;
        dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract + MOD) % MOD;
    }
    return (int)dp[n];
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n) {  // 특수 배치의 중복을 뺀 타일링 점화식 계산
// const long long MOD = 1000000007; vector<long long> dp(n + 4, 0);  // 너비별 타일링 수 저장
// dp[0] = 1; dp[1] = 1; dp[2] = 3; dp[3] = 10;  // 너비 0부터 3까지의 초기 경우의 수
// for (int width = 4; width <= n; ++width) {  // 큰 너비를 순서대로 계산
// long long subtract = width >= 6 ? dp[width - 6] : 0;  // 겹쳐 센 여섯 칸 이전의 항을 준비
// dp[width] = (dp[width - 1] + 2 * dp[width - 2] + 6 * dp[width - 3] + dp[width - 4] - subtract + MOD) % MOD;  // 기본 배치와 특수 배치의 점화식을 나머지로 계산
// }  // 블록 끝
// return (int)dp[n];  // 요청 너비의 타일링 수 반환
// }  // 블록 끝

// 풀이 요약
// 작은 너비의 초기값에서 기본 및 특수 타일 배치의 점화식을 적용하고 중복된 여섯 칸 이전 항 빼기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/017_181186_%EC%95%84%EB%B0%A9%EA%B0%80%EB%A5%B4%EB%93%9C_%ED%83%80%EC%9D%BC%EB%A7%81/README.md)
