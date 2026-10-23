# 등굣길

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42898) · Level 3 · C++

## 풀이

물웅덩이의 경로 수는 0으로 두고 각 칸에서 위와 왼쪽의 최단 경로 수를 더하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(int m, int n, vector<vector<int>> puddles) {
    vector<vector<bool>> blocked(n + 1, vector<bool>(m + 1, false));
    for (const auto& point : puddles) blocked[point[1]][point[0]] = true;
    vector<int> dp(m + 1, 0); dp[1] = 1; const int MOD = 1000000007;
    for (int y = 1; y <= n; ++y) for (int x = 1; x <= m; ++x) {
        if (blocked[y][x]) dp[x] = 0;
        else dp[x] = (dp[x] + dp[x - 1]) % MOD;
    }
    return dp[m];
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int m, int n, vector<vector<int>> puddles) {  // 물웅덩이를 피해 오는 최단 경로 수 누적
// vector<vector<bool>> blocked(n + 1, vector<bool>(m + 1, false));  // 물에 잠긴 위치 저장
// for (const auto& point : puddles) blocked[point[1]][point[0]] = true;  // x와 y를 열과 행에 맞게 등록
// vector<int> dp(m + 1, 0); dp[1] = 1; const int MOD = 1000000007;  // 열별 최단 경로 수와 나머지 기준 초기화
// for (int y = 1; y <= n; ++y) for (int x = 1; x <= m; ++x) {  // 오른쪽과 아래쪽으로만 이동하는 경로 계산
// if (blocked[y][x]) dp[x] = 0;  // 물웅덩이는 도달 경로가 없음
// else dp[x] = (dp[x] + dp[x - 1]) % MOD;  // 위와 왼쪽에서 오는 두 경로 수를 더하기
// }  // 블록 끝
// return dp[m];  // 학교까지의 최단 경로 수 반환
// }  // 블록 끝

// 풀이 요약
// 물웅덩이의 경로 수는 0으로 두고 각 칸에서 위와 왼쪽의 최단 경로 수를 더하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:44:06
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/063_42898_%EB%93%B1%EA%B5%A3%EA%B8%B8/README.md)
