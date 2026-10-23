# 숫자 야구

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/451808) · Level 3 · C++

## 풀이

모든 비밀번호 후보의 응답 표를 필요할 때 만들고 가장 큰 응답 그룹이 작아지는 추측을 선택하며 실제 응답과 맞는 후보만 남기기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <algorithm>
#include <array>
#include <functional>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
extern string submit(int);

int solution(int n) {
    vector<array<int, 4>> digits; vector<int> masks, numbers;
    for (int a = 1; a <= 9; ++a) for (int b = 1; b <= 9; ++b) if (b != a) for (int c = 1; c <= 9; ++c) if (c != a && c != b) for (int d = 1; d <= 9; ++d) if (d != a && d != b && d != c) {
        digits.push_back({a, b, c, d}); masks.push_back((1 << a) | (1 << b) | (1 << c) | (1 << d)); numbers.push_back(1000 * a + 100 * b + 10 * c + d);
    }
    vector<vector<unsigned char>> cache(digits.size());
    auto feedback_row = [&](int index) -> const vector<unsigned char>& {
        auto& row = cache[index];
        if (row.empty()) {
            row.resize(digits.size());
            for (int i = 0; i < (int)digits.size(); ++i) {
                int strikes = 0; for (int j = 0; j < 4; ++j) strikes += digits[index][j] == digits[i][j];
                int common = __builtin_popcount((unsigned)(masks[index] & masks[i]));
                row[i] = (unsigned char)(common * 5 + strikes);
            }
        }
        return row;
    };
    vector<int> candidates(digits.size()); iota(candidates.begin(), candidates.end(), 0);
    for (int turn = 0; turn < n; ++turn) {
        if (candidates.size() == 1) return numbers[candidates[0]];
        int selected = candidates[0];
        if (turn > 0) {
            int best = (int)candidates.size() + 1;
            for (int guess : candidates) {
                const auto& row = feedback_row(guess); array<int, 25> counts{}; int worst = 0;
                for (int hidden : candidates) { worst = max(worst, ++counts[row[hidden]]); if (worst >= best) break; }
                if (worst < best) { best = worst; selected = guess; if (best == 1) break; }
            }
        }
        string clue = submit(numbers[selected]);
        int strikes = clue[0] - '0', balls = clue[3] - '0', observed = (strikes + balls) * 5 + strikes;
        const auto& row = feedback_row(selected); vector<int> next;
        for (int hidden : candidates) if (row[hidden] == observed) next.push_back(hidden);
        candidates = move(next);
    }
    return numbers[candidates[0]];
}

// 전체 코드 줄별 설명
// #include <algorithm>  // 정렬·이분 탐색·최댓값 같은 표준 알고리즘
// #include <array>  // 크기가 고정된 array
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// #include <string>  // 문자열을 담는 string
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// extern string submit(int);  // 채점 환경의 숫자 야구 응답 함수를 외부 선언
// int solution(int n) {  // 응답별 후보 수를 줄여 숫자 야구 비밀번호 찾기
// vector<array<int, 4>> digits; vector<int> masks, numbers;  // 가능한 네 자리 패턴과 자릿수 집합 및 실제 정수 저장
// for (int a = 1; a <= 9; ++a) for (int b = 1; b <= 9; ++b) if (b != a) for (int c = 1; c <= 9; ++c) if (c != a && c != b) for (int d = 1; d <= 9; ++d) if (d != a && d != b && d != c) {  // 0 없이 서로 다른 네 숫자의 모든 순열 만들기
// digits.push_back({a, b, c, d}); masks.push_back((1 << a) | (1 << b) | (1 << c) | (1 << d)); numbers.push_back(1000 * a + 100 * b + 10 * c + d);  // 각 패턴의 세 표현을 나란히 저장
// }  // 블록 끝
// vector<vector<unsigned char>> cache(digits.size());  // 추측별 모든 비밀번호의 응답을 필요할 때 계산
// auto feedback_row = [&](int index) -> const vector<unsigned char>& {  // 한 추측의 응답 표를 참조로 반환
// auto& row = cache[index];  // 해당 추측의 캐시 공간을 참조
// if (row.empty()) {  // 아직 계산하지 않은 추측만 전체 응답 구하기
// row.resize(digits.size());  // 모든 후보에 대한 응답 바이트를 할당
// for (int i = 0; i < (int)digits.size(); ++i) {  // 각 후보 비밀번호의 피드백 계산
// int strikes = 0; for (int j = 0; j < 4; ++j) strikes += digits[index][j] == digits[i][j];  // 자리와 숫자가 모두 같은 스트라이크 수 세기
// int common = __builtin_popcount((unsigned)(masks[index] & masks[i]));  // 공통 숫자 수를 비트 AND로 세기
// row[i] = (unsigned char)(common * 5 + strikes);  // 공통 숫자 수와 스트라이크 수를 한 바이트 응답으로 합치기
// }  // 블록 끝
// }  // 블록 끝
// return row;  // 계산하거나 기억한 응답 표 반환
// };  // 블록 끝
// vector<int> candidates(digits.size()); iota(candidates.begin(), candidates.end(), 0);  // 처음에는 모든 패턴을 비밀번호 후보로 두기
// for (int turn = 0; turn < n; ++turn) {  // 허용된 호출 횟수 안에서 후보 줄이기
// if (candidates.size() == 1) return numbers[candidates[0]];  // 후보가 하나이면 추가 호출 없이 답 반환
// int selected = candidates[0];  // 첫 추측 또는 최소 분할 후보 초기화
// if (turn > 0) {  // 첫 호출 이후에는 최악의 후보 수가 적은 추측 고르기
// int best = (int)candidates.size() + 1;  // 현재 최소 최악 분할 크기 초기화
// for (int guess : candidates) {  // 남은 후보를 추측으로 사용해 보기
// const auto& row = feedback_row(guess); array<int, 25> counts{}; int worst = 0;  // 응답별 후보 수와 최대 크기 초기화
// for (int hidden : candidates) { worst = max(worst, ++counts[row[hidden]]); if (worst >= best) break; }  // 응답 분할을 세다가 기존 최선보다 나쁘면 중단
// if (worst < best) { best = worst; selected = guess; if (best == 1) break; }  // 더 균등하게 나누는 추측 선택
// }  // 블록 끝
// }  // 블록 끝
// string clue = submit(numbers[selected]);  // 선택한 숫자를 외부 채점 함수에 제출
// int strikes = clue[0] - '0', balls = clue[3] - '0', observed = (strikes + balls) * 5 + strikes;  // 문자열 응답을 내부 피드백 번호로 바꾸기
// const auto& row = feedback_row(selected); vector<int> next;  // 현재 추측의 표와 다음 후보 목록을 준비
// for (int hidden : candidates) if (row[hidden] == observed) next.push_back(hidden);  // 실제 응답과 일치하는 후보만 남기기
// candidates = move(next);  // 줄어든 후보 목록 적용
// }  // 블록 끝
// return numbers[candidates[0]];  // 남은 후보가 가리키는 비밀번호 반환
// }  // 블록 끝

// 풀이 요약
// 모든 비밀번호 후보의 응답 표를 필요할 때 만들고 가장 큰 응답 그룹이 작아지는 추측을 선택하며 실제 응답과 맞는 후보만 남기기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:44:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/007_451808_%EC%88%AB%EC%9E%90_%EC%95%BC%EA%B5%AC/README.md)
