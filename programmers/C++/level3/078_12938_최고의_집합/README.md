# 최고의 집합

[레벨 3 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12938) · Level 3 · C++

## 풀이

합을 n으로 나눈 몫을 기본 원소로 두고 나머지 개수만큼 1을 더해 곱이 최대가 되도록 고르게 나누기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <vector>
using namespace std;

vector<int> solution(int n, int s) {
    if (s < n) return {-1};
    int quotient = s / n, remainder = s % n;
    vector<int> answer(n, quotient);
    for (int i = n - remainder; i < n; ++i) ++answer[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <vector>  // 크기를 바꿀 수 있는 연속 배열 vector
// using namespace std;  // std:: 접두사 생략
// vector<int> solution(int n, int s) {  // 합을 최대한 고르게 나눠 원소의 곱 최대화
// if (s < n) return {-1};  // 양의 정수 n개의 최소 합보다 작으면 집합이 없음
// int quotient = s / n, remainder = s % n;  // 원소를 최대한 고르게 나눌 몫과 나머지 구하기
// vector<int> answer(n, quotient);  // 모든 원소를 몫으로 초기화
// for (int i = n - remainder; i < n; ++i) ++answer[i];  // 뒤쪽 나머지 개수만큼 1을 더해 오름차순 유지
// return answer;  // 합이 s이고 곱이 최대인 집합 반환
// }  // 블록 끝

// 풀이 요약
// 합을 n으로 나눈 몫을 기본 원소로 두고 나머지 개수만큼 1을 더해 곱이 최대가 되도록 고르게 나누기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/078_12938_%EC%B5%9C%EA%B3%A0%EC%9D%98_%EC%A7%91%ED%95%A9/README.md)
