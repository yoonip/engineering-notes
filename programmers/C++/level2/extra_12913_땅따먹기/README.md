# 땅따먹기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12913) · Level 2 · C++

## 풀이

이전 행의 다른 열에서 얻은 점수 중 최댓값에 현재 칸의 점수를 더해 행별 최대 점수 갱신

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <vector>
using namespace std;

int solution(vector<vector<int>> land) {
    array<int, 4> previous{0, 0, 0, 0};
    for (const auto& row : land) {
        array<int, 4> current{0, 0, 0, 0};
        for (int column = 0; column < 4; ++column) for (int before = 0; before < 4; ++before) if (column != before) current[column] = max(current[column], previous[before] + row[column]);
        previous = current;
    }
    return *max_element(previous.begin(), previous.end());
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> land) {  // 직전 행의 다른 열 중 최대 점수에서 이어가기
// array<int, 4> previous{0, 0, 0, 0};  // 이전 행의 각 열까지 얻은 최대 점수 저장
// for (const auto& row : land) {  // 위 행부터 차례대로 내려오기
// array<int, 4> current{0, 0, 0, 0};  // 현재 행의 새 점수 저장
// for (int column = 0; column < 4; ++column) for (int before = 0; before < 4; ++before) if (column != before) current[column] = max(current[column], previous[before] + row[column]);  // 직전과 다른 열에서 온 경우 중 최댓값 고르기
// previous = current;  // 현재 행의 결과를 다음 행의 기준으로 사용
// }  // 블록 끝
// return *max_element(previous.begin(), previous.end());  // 마지막 행의 최대 점수 반환
// }  // 블록 끝

// 풀이 요약
// 이전 행의 다른 열에서 얻은 점수 중 최댓값에 현재 칸의 점수를 더해 행별 최대 점수 갱신
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:42:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12913_%EB%95%85%EB%94%B0%EB%A8%B9%EA%B8%B0/README.md)
