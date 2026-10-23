# 주사위 게임 2

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181930) · Level 0 · C++

## 풀이

같은 눈의 수에 따라 1차 합에 제곱 합과 세제곱 합을 차례대로 곱하기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int a, int b, int c) {
    int answer = a + b + c;
    if (a == b || b == c || a == c) answer *= a * a + b * b + c * c;
    if (a == b && b == c) answer *= a * a * a + b * b * b + c * c * c;
    return answer;
}

// 전체 코드 줄별 설명
// int solution(int a, int b, int c) {  // 주사위 게임 2 풀이 시작
//     int answer = a + b + c;  // 세 주사위 눈의 합으로 기본 점수를 초기화
//     if (a == b || b == c || a == c) answer *= a * a + b * b + c * c;  // ||로 같은 눈이 있는지 검사하고 *=로 제곱의 합을 점수에 곱하기
//     if (a == b && b == c) answer *= a * a * a + b * b * b + c * c * c;  // &&로 세 눈이 모두 같은지 검사하고 *=로 세제곱의 합을 점수에 곱하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 같은 눈의 수에 따라 1차 합에 제곱 합과 세제곱 합을 차례대로 곱하기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:37:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181930_%EC%A3%BC%EC%82%AC%EC%9C%84_%EA%B2%8C%EC%9E%84_2/README.md)
