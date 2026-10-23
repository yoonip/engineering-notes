# [PCCP 기출문제] 2번 / 퍼즐 게임 챌린지

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340212) · Level 2 · C++

## 풀이

숙련도를 이분 탐색하고 각 후보에서 실패와 재풀이 시간을 합산해 시간 제한을 만족하는지 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<int> diffs, vector<int> times, long long limit) {
    int left = 1, right = *max_element(diffs.begin(), diffs.end());
    while (left < right) {
        int level = left + (right - left) / 2;
        long long elapsed = 0;
        for (int i = 0; i < (int)diffs.size(); ++i) {
            elapsed += times[i];
            if (diffs[i] > level) elapsed += 1LL * (diffs[i] - level) * (times[i] + (i ? times[i - 1] : 0));
            if (elapsed > limit) break;
        }
        if (elapsed <= limit) right = level;
        else left = level + 1;
    }
    return left;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> diffs, vector<int> times, long long limit) {  // 제한 시간 안에 풀 수 있는 최소 숙련도 찾기
// int left = 1, right = *max_element(diffs.begin(), diffs.end());  // 숙련도의 이분 탐색 범위를 설정하기
// while (left < right) {  // 시간 제한을 만족하는 최소 숙련도 찾기
// int level = left + (right - left) / 2;  // 중간 숙련도 선택
// long long elapsed = 0;  // 총 소요 시간을 넓은 정수형으로 누적
// for (int i = 0; i < (int)diffs.size(); ++i) {  // 퍼즐을 순서대로 처리
// elapsed += times[i];  // 현재 퍼즐을 한 번 푸는 시간을 더하기
// if (diffs[i] > level) elapsed += 1LL * (diffs[i] - level) * (times[i] + (i ? times[i - 1] : 0));  // 실패 횟수만큼 현재 퍼즐과 직전 퍼즐의 시간을 더하기
// if (elapsed > limit) break;  // 제한을 넘으면 더 계산하지 않음
// }  // 블록 끝
// if (elapsed <= limit) right = level;  // 가능하면 더 낮은 숙련도 찾기
// else left = level + 1;  // 불가능하면 숙련도를 높
// }  // 블록 끝
// return left;  // 가능한 최소 숙련도 반환
// }  // 블록 끝

// 풀이 요약
// 숙련도를 이분 탐색하고 각 후보에서 실패와 재풀이 시간을 합산해 시간 제한을 만족하는지 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:26:28
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/009_340212_%ED%8D%BC%EC%A6%90_%EA%B2%8C%EC%9E%84_%EC%B1%8C%EB%A6%B0%EC%A7%80/README.md)
