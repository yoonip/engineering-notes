# 카운트 다운

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131129) · Level 3 · C++

## 풀이

점수별 최소 다트 수를 구하고 같은 수의 다트라면 싱글 및 불 횟수가 큰 상태 선택

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int target) {
    vector<int> throws(target + 1, target + 1), singles(target + 1, 0); throws[0] = 0;
    vector<int> scores;
    for (int score = 1; score <= 60; ++score) if (score <= 20 || (score % 2 == 0 && score <= 40) || score % 3 == 0 || score == 50) scores.push_back(score);
    for (int total = 1; total <= target; ++total) for (int score : scores) {
        if (score > total) break;
        int count = throws[total - score] + 1, good = singles[total - score] + (score <= 20 || score == 50);
        if (count < throws[total] || (count == throws[total] && good > singles[total])) { throws[total] = count; singles[total] = good; }
    }
    return {throws[target], singles[target]};
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int target) {  // 다트 수 최소, 동률이면 싱글·불 횟수 최대화
// vector<int> throws(target + 1, target + 1), singles(target + 1, 0); throws[0] = 0;  // 점수별 최소 다트 수와 최대 싱글 및 불 수 저장
// vector<int> scores;  // 한 번에 얻을 수 있는 중복 없는 점수 만들기
// for (int score = 1; score <= 60; ++score) if (score <= 20 || (score % 2 == 0 && score <= 40) || score % 3 == 0 || score == 50) scores.push_back(score);  // 싱글, 더블, 트리플, 불 점수 등록
// for (int total = 1; total <= target; ++total) for (int score : scores) {  // 작은 목표 점수부터 다트 한 번 추가
// if (score > total) break;  // 목표를 넘는 점수는 더 검사하지 않음
// int count = throws[total - score] + 1, good = singles[total - score] + (score <= 20 || score == 50);  // 새 다트 수와 우선 점수의 횟수 구하기
// if (count < throws[total] || (count == throws[total] && good > singles[total])) { throws[total] = count; singles[total] = good; }  // 다트 수를 최소화하고 동률에서 싱글 및 불 최대화
// }  // 블록 끝
// return {throws[target], singles[target]};  // 최적 다트 수와 싱글 및 불 수 반환
// }  // 블록 끝

// 풀이 요약
// 점수별 최소 다트 수를 구하고 같은 수의 다트라면 싱글 및 불 횟수가 큰 상태 선택
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/029_131129_%EC%B9%B4%EC%9A%B4%ED%8A%B8_%EB%8B%A4%EC%9A%B4/README.md)
