# 인사고과

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/152995) · Level 3 · C++

## 풀이

첫 점수 내림차순과 둘째 점수 오름차순으로 정렬해 탈락 직원을 제외하고 완호보다 합계가 큰 유효 직원 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <vector>
using namespace std;

int solution(vector<vector<int>> scores) {
    vector<int> target = scores[0]; int target_sum = target[0] + target[1];
    sort(scores.begin(), scores.end(), [](const auto& a, const auto& b) { return a[0] != b[0] ? a[0] > b[0] : a[1] < b[1]; });
    int rank = 1, best_second = -1;
    for (const auto& score : scores) {
        if (score[1] < best_second) { if (score == target) return -1; continue; }
        best_second = score[1];
        if (score[0] + score[1] > target_sum) ++rank;
    }
    return rank;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<vector<int>> scores) {  // 지배당한 직원을 빼고 완호의 점수 순위 계산
// vector<int> target = scores[0]; int target_sum = target[0] + target[1];  // 완호의 두 점수와 합계 저장
// sort(scores.begin(), scores.end(), [](const auto& a, const auto& b) { return a[0] != b[0] ? a[0] > b[0] : a[1] < b[1]; });  // 첫 점수 내림차순과 둘째 점수 오름차순으로 정렬
// int rank = 1, best_second = -1;  // 완호의 순위와 지금까지 유효한 둘째 점수의 최댓값 초기화
// for (const auto& score : scores) {  // 두 점수가 모두 더 높은 사람이 있는지 검사
// if (score[1] < best_second) { if (score == target) return -1; continue; }  // 탈락 대상은 제외하고 완호이면 -1 반환
// best_second = score[1];  // 현재까지의 둘째 점수 경계 갱신
// if (score[0] + score[1] > target_sum) ++rank;  // 합계가 완호보다 큰 유효 직원 세기
// }  // 블록 끝
// return rank;  // 완호의 최종 순위 반환
// }  // 블록 끝

// 풀이 요약
// 첫 점수 내림차순과 둘째 점수 오름차순으로 정렬해 탈락 직원을 제외하고 완호보다 합계가 큰 유효 직원 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/019_152995_%EC%9D%B8%EC%82%AC%EA%B3%A0%EA%B3%BC/README.md)
