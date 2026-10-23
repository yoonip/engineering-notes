# 연속 부분 수열 합의 개수

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131701) · Level 2 · C++

## 풀이

원형 수열의 모든 시작 위치와 길이를 순회하며 누적합을 집합에 넣어 서로 다른 합의 개수 세기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <unordered_set>
#include <vector>
using namespace std;

int solution(vector<int> elements) {
    int n = (int)elements.size();
    unordered_set<int> sums;
    for (int start = 0; start < n; ++start) {
        int total = 0;
        for (int length = 1; length <= n; ++length) {
            total += elements[(start + length - 1) % n];
            sums.insert(total);
        }
    }
    return (int)sums.size();
}

// 전체 코드 줄별 설명
// #include <unordered_set>  // 중복을 걸러 낼 해시 집합
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// int solution(vector<int> elements) {  // 원형 수열의 서로 다른 연속 구간 합 세기
// int n = (int)elements.size();  // 원형 수열의 길이 구하기
// unordered_set<int> sums;  // 중복 없는 부분 수열의 합 저장
// for (int start = 0; start < n; ++start) {  // 원형 수열의 모든 시작 위치 고르기
// int total = 0;  // 현재 시작 위치의 누적합 초기화
// for (int length = 1; length <= n; ++length) {  // 길이 1부터 전체 길이까지 늘리기
// total += elements[(start + length - 1) % n];  // 나머지 연산으로 원형 인덱스를 계산해 다음 값을 더하기
// sums.insert(total);  // 현재 부분 수열의 합을 집합에 넣기
// }  // 블록 끝
// }  // 블록 끝
// return (int)sums.size();  // 서로 다른 합의 개수 반환
// }  // 블록 끝

// 풀이 요약
// 원형 수열의 모든 시작 위치와 길이를 순회하며 누적합을 집합에 넣어 서로 다른 합의 개수 세기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:54
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/040_131701_%EC%97%B0%EC%86%8D_%EB%B6%80%EB%B6%84_%EC%88%98%EC%97%B4_%ED%95%A9%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
