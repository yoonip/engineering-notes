# 간단한 논리 연산

[레벨 0 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181917) · Level 0 · C++

## 풀이

두 쌍의 논리합을 각각 구한 뒤 두 결과의 논리곱을 반환

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
bool solution(bool x1, bool x2, bool x3, bool x4) {
    return (x1 || x2) && (x3 || x4);
}

// 전체 코드 줄별 설명
// bool solution(bool x1, bool x2, bool x3, bool x4) {  // 간단한 논리 연산 풀이 시작
//     return (x1 || x2) && (x3 || x4);  // ||로 각 쌍의 논리합을 구하고 &&로 두 결과의 논리곱을 반환
// }  // 블록 끝

// 풀이 요약
// 두 쌍의 논리합을 각각 구한 뒤 두 결과의 논리곱을 반환
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:47:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181917_%EA%B0%84%EB%8B%A8%ED%95%9C_%EB%85%BC%EB%A6%AC_%EC%97%B0%EC%82%B0/README.md)
