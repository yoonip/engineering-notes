# 소수 찾기

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42839) · Level 2 · C++

## 풀이

숫자 조각의 모든 길이와 순열로 중복 없는 정수를 만들고 각 후보의 제곱근까지 약수 검사

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <functional>
#include <string>
#include <unordered_set>
#include <vector>
using namespace std;

int solution(string numbers) {
    vector<bool> used(numbers.size(), false);
    unordered_set<int> candidates;
    function<void(int)> dfs = [&](int value) {
        for (int i = 0; i < (int)numbers.size(); ++i) if (!used[i]) {
            int next = value * 10 + numbers[i] - '0';
            candidates.insert(next); used[i] = true;
            dfs(next);
            used[i] = false;
        }
    };
    dfs(0);
    int answer = 0;
    for (int value : candidates) {
        bool prime = value >= 2;
        for (int divisor = 2; divisor <= value / divisor; ++divisor) if (value % divisor == 0) { prime = false; break; }
        answer += prime;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <functional>  // 재귀 람다를 담는 function과 함수 객체
// #include <string>  // 문자열을 담는 string
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(string numbers) {  // 숫자 조각의 순열로 만든 정수를 소수 판정
// vector<bool> used(numbers.size(), false);  // 이미 사용한 종이 조각의 위치를 표시
// unordered_set<int> candidates;  // 선행 0과 중복 조각으로 생기는 같은 정수 합치기
// function<void(int)> dfs = [&](int value) {  // 현재 정수 뒤에 사용하지 않은 숫자를 이어 붙이기
// for (int i = 0; i < (int)numbers.size(); ++i) if (!used[i]) {  // 아직 쓰지 않은 종이 조각 고르기
// int next = value * 10 + numbers[i] - '0';  // 현재 수에 새 자릿수 붙이기
// candidates.insert(next); used[i] = true;  // 새 정수를 등록하고 조각을 사용 처리
// dfs(next);  // 더 긴 정수도 생성
// used[i] = false;  // 다른 순열을 위해 사용 표시 되돌리기
// }  // 블록 끝
// };  // 블록 끝
// dfs(0);  // 빈 숫자에서 모든 길이의 순열을 생성
// int answer = 0;  // 소수의 개수 초기화
// for (int value : candidates) {  // 중복 없는 후보 정수 검사
// bool prime = value >= 2;  // 2 미만은 소수에서 제외
// for (int divisor = 2; divisor <= value / divisor; ++divisor) if (value % divisor == 0) { prime = false; break; }  // 제곱근까지 약수 검사
// answer += prime;  // 소수인 후보를 하나 세기
// }  // 블록 끝
// return answer;  // 만들 수 있는 소수의 개수 반환
// }  // 블록 끝

// 풀이 요약
// 숫자 조각의 모든 길이와 순열로 중복 없는 정수를 만들고 각 후보의 제곱근까지 약수 검사
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/076_42839_%EC%86%8C%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
