# 멀쩡한 사각형

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/62048) · Level 2 · C++

## 풀이

전체 사각형 넓이에서 대각선이 지나는 w+h-gcd(w,h)개의 칸 빼기

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
#include <numeric>
using namespace std;

long long solution(int w, int h) {
    long long broken = 1LL * w + h - gcd(w, h);
    return 1LL * w * h - broken;
}

// 전체 코드 줄별 설명
// #include <numeric>  // 누적합·최대공약수 같은 수치 알고리즘
// using namespace std;  // std:: 접두사 생략
// long long solution(int w, int h) {  // 대각선이 지나는 칸 수를 전체 넓이에서 빼기
// long long broken = 1LL * w + h - gcd(w, h);  // 격자선을 지나는 대각선이 훼손하는 칸 수 구하기
// return 1LL * w * h - broken;  // 전체 칸 수에서 훼손된 칸 수 빼기
// }  // 블록 끝

// 풀이 요약
// 전체 사각형 넓이에서 대각선이 지나는 w+h-gcd(w,h)개의 칸 빼기
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/064_62048_%EB%A9%80%EC%A9%A1%ED%95%9C_%EC%82%AC%EA%B0%81%ED%98%95/README.md)
