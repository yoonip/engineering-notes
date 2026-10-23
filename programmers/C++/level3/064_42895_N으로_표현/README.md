# N으로 표현

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42895) · Level 3 · C++

## 풀이

N 사용 개수별 결과 집합을 만들고 두 부분 식의 사칙연산과 숫자 이어 붙이기를 조합해 목표 수 찾기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <unordered_set>
#include <vector>
using namespace std;

int solution(int N, int number) {
    vector<unordered_set<int>> values(9); int repeated = 0;
    for (int count = 1; count <= 8; ++count) {
        repeated = repeated * 10 + N; values[count].insert(repeated);
        for (int left = 1; left < count; ++left) for (int first : values[left]) for (int second : values[count - left]) {
            values[count].insert(first + second); values[count].insert(first - second); values[count].insert(first * second);
            if (second != 0) values[count].insert(first / second);
        }
        if (values[count].count(number)) return count;
    }
    return -1;
}

// 전체 코드 줄별 설명
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(int N, int number) {  // N 사용 개수별 사칙연산 결과 집합 확장
// vector<unordered_set<int>> values(9); int repeated = 0;  // N 사용 개수별 만들 수 있는 정수와 이어 붙인 수 저장
// for (int count = 1; count <= 8; ++count) {  // 적은 N 사용 수부터 검사
// repeated = repeated * 10 + N; values[count].insert(repeated);  // N을 현재 개수만큼 이어 붙인 수 넣기
// for (int left = 1; left < count; ++left) for (int first : values[left]) for (int second : values[count - left]) {  // 두 부분 식의 N 개수를 나누어 모든 결과를 조합
// values[count].insert(first + second); values[count].insert(first - second); values[count].insert(first * second);  // 덧셈, 뺄셈, 곱셈 결과 넣기
// if (second != 0) values[count].insert(first / second);  // 0으로 나누지 않는 정수 나눗셈 결과 넣기
// }  // 블록 끝
// if (values[count].count(number)) return count;  // 목표 수가 만들어지면 현재 사용 개수가 최소
// }  // 블록 끝
// return -1;  // 여덟 번 안에 표현할 수 없으면 -1 반환
// }  // 블록 끝

// 풀이 요약
// N 사용 개수별 결과 집합을 만들고 두 부분 식의 사칙연산과 숫자 이어 붙이기를 조합해 목표 수 찾기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:44:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/064_42895_N%EC%9C%BC%EB%A1%9C_%ED%91%9C%ED%98%84/README.md)
