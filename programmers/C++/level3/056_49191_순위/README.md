# 순위

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49191) · Level 3 · C++

## 풀이

경기 승패 관계의 전이 폐쇄를 구한 뒤 다른 모든 선수와 우열을 알 수 있는 선수의 순위를 확정하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

int solution(int n, vector<vector<int>> results) {
    vector<vector<bool>> wins(n, vector<bool>(n, false));
    for (const auto& result : results) wins[result[0] - 1][result[1] - 1] = true;
    for (int middle = 0; middle < n; ++middle) for (int first = 0; first < n; ++first) if (wins[first][middle]) for (int last = 0; last < n; ++last) if (wins[middle][last]) wins[first][last] = true;
    int answer = 0;
    for (int player = 0; player < n; ++player) { int known = 0; for (int other = 0; other < n; ++other) known += wins[player][other] || wins[other][player]; answer += known == n - 1; }
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int n, vector<vector<int>> results) {  // 승패의 전이 관계로 순위가 확정되는 선수 세기
// vector<vector<bool>> wins(n, vector<bool>(n, false));  // 각 선수가 다른 선수보다 앞선다는 관계 저장
// for (const auto& result : results) wins[result[0] - 1][result[1] - 1] = true;  // 직접 경기 결과 등록
// for (int middle = 0; middle < n; ++middle) for (int first = 0; first < n; ++first) if (wins[first][middle]) for (int last = 0; last < n; ++last) if (wins[middle][last]) wins[first][last] = true;  // 승리 관계의 전이 폐쇄 구하기
// int answer = 0;  // 순위가 확정되는 선수 수 초기화
// for (int player = 0; player < n; ++player) { int known = 0; for (int other = 0; other < n; ++other) known += wins[player][other] || wins[other][player]; answer += known == n - 1; }  // 다른 모든 선수와의 우열을 알면 확정 순위로 세기
// return answer;  // 순위를 확정할 수 있는 선수 수 반환
// }  // 블록 끝

// 풀이 요약
// 경기 승패 관계의 전이 폐쇄를 구한 뒤 다른 모든 선수와 우열을 알 수 있는 선수의 순위를 확정하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/056_49191_%EC%88%9C%EC%9C%84/README.md)
