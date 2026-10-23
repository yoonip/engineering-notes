# 억억단을 외우자

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/138475) · Level 3 · C++

## 풀이

소수 거듭제곱으로 정수별 약수 수를 계산하고 시작값이 큰 질의부터 구간을 확장하며 최빈 등장 정수를 추적

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

vector<int> solution(int e, vector<int> starts) {
    vector<int> divisors(e + 1, 1);
    for (int prime = 2; prime <= e; ++prime) if (divisors[prime] == 1) {
        long long power = prime; int exponent = 1;
        while (power <= e) {
            for (long long multiple = power; multiple <= e; multiple += power) divisors[(size_t)multiple] = divisors[(size_t)multiple] / exponent * (exponent + 1);
            power *= prime; ++exponent;
        }
    }
    vector<pair<int, int>> queries;
    for (int i = 0; i < (int)starts.size(); ++i) queries.push_back({starts[i], i});
    sort(queries.rbegin(), queries.rend());
    vector<int> answer(starts.size()); int cursor = e, winner = e, best_count = divisors[e];
    for (auto [start, index] : queries) {
        while (cursor >= start) { if (divisors[cursor] >= best_count) { winner = cursor; best_count = divisors[cursor]; } --cursor; }
        answer[index] = winner;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int e, vector<int> starts) {  // 약수 수와 동률 번호 기준으로 구간 최빈값 찾기
// vector<int> divisors(e + 1, 1);  // 각 정수의 약수 개수를 1로 초기화
// for (int prime = 2; prime <= e; ++prime) if (divisors[prime] == 1) {  // 아직 다른 소인수로 갱신되지 않은 소수 찾기
// long long power = prime; int exponent = 1;  // 현재 소수의 거듭제곱과 지수 초기화
// while (power <= e) {  // 범위 안의 모든 소수 거듭제곱 처리
// for (long long multiple = power; multiple <= e; multiple += power) divisors[(size_t)multiple] = divisors[(size_t)multiple] / exponent * (exponent + 1);  // 해당 소수의 지수 증가를 약수 개수에 반영
// power *= prime; ++exponent;  // 다음 거듭제곱과 지수로 이동
// }  // 블록 끝
// }  // 블록 끝
// vector<pair<int, int>> queries;  // 시작값과 원래 질의 인덱스를 함께 저장
// for (int i = 0; i < (int)starts.size(); ++i) queries.push_back({starts[i], i});  // 질의를 정렬할 배열에 넣기
// sort(queries.rbegin(), queries.rend());  // 시작값이 큰 질의부터 처리
// vector<int> answer(starts.size()); int cursor = e, winner = e, best_count = divisors[e];  // 오른쪽 끝부터 최빈 등장 정수를 추적
// for (auto [start, index] : queries) {  // 구간의 왼쪽 끝을 줄여 가며 답 만들기
// while (cursor >= start) { if (divisors[cursor] >= best_count) { winner = cursor; best_count = divisors[cursor]; } --cursor; }  // 약수 수가 같으면 더 작은 정수로 갱신
// answer[index] = winner;  // 원래 질의 순서의 위치에 답 넣기
// }  // 블록 끝
// return answer;  // 각 구간에서 가장 많이 나타나는 최소 정수 반환
// }  // 블록 끝

// 풀이 요약
// 소수 거듭제곱으로 정수별 약수 수를 계산하고 시작값이 큰 질의부터 구간을 확장하며 최빈 등장 정수를 추적
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:50:05
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/023_138475_%EC%96%B5%EC%96%B5%EB%8B%A8%EC%9D%84_%EC%99%B8%EC%9A%B0%EC%9E%90/README.md)
