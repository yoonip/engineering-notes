# 타겟 넘버

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/43165) · Level 2 · C++

## 풀이

각 숫자에 양수와 음수 부호를 붙이는 두 선택으로 합별 방법 수 누적

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <unordered_map>
#include <utility>
#include <vector>
using namespace std;

int solution(vector<int> numbers, int target) {
    unordered_map<int, int> ways{{0, 1}};
    for (int number : numbers) {
        unordered_map<int, int> next;
        for (const auto& entry : ways) { next[entry.first + number] += entry.second; next[entry.first - number] += entry.second; }
        ways = move(next);
    }
    return ways[target];
}

// 전체 코드 줄별 설명
// #include <unordered_map>  // 키로 값을 찾는 해시 맵
// #include <utility>  // 두 값을 묶는 pair와 이동 유틸리티
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> numbers, int target) {  // 숫자마다 두 부호를 골라 목표 합의 경우의 수 계산
// unordered_map<int, int> ways{{0, 1}};  // 합 0을 만드는 빈 선택 한 가지로 시작
// for (int number : numbers) {  // 각 수에 양수와 음수 부호 붙이기
// unordered_map<int, int> next;  // 현재 수까지 처리한 합별 방법 수 저장
// for (const auto& entry : ways) { next[entry.first + number] += entry.second; next[entry.first - number] += entry.second; }  // 두 부호의 새 합에 기존 방법 수를 더하기
// ways = move(next);  // 다음 단계의 기준 상태로 바꾸기
// }  // 블록 끝
// return ways[target];  // 목표 합을 만드는 방법 수 반환
// }  // 블록 끝

// 풀이 요약
// 각 숫자에 양수와 음수 부호를 붙이는 두 선택으로 합별 방법 수 누적
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/069_43165_%ED%83%80%EA%B2%9F_%EB%84%98%EB%B2%84/README.md)
