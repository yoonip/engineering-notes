# 3 x n 타일링

[레벨 2 목록](../README.md) · [C++ 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12902) · Level 2 · C++

## 풀이

짝수 너비에서 앞선 두 짝수 너비의 경우의 수를 4배와 뺄셈으로 연결하는 점화식 적용

## 코드와 줄별 설명

[코드 파일](solution.cpp) · [채점 기록](grading.json)

```cpp
int solution(int n) {
    if (n % 2) return 0;
    const long long MOD = 1000000007;
    long long previous = 1, current = 3;
    for (int width = 4; width <= n; width += 2) {
        long long next = (4 * current - previous + MOD) % MOD;
        previous = current; current = next;
    }
    return (int)current;
}

// 전체 코드 줄별 설명
// int solution(int n) {  // 짝수 너비의 3행 타일링 점화식 계산
// if (n % 2) return 0;  // 너비가 홀수이면 3×n 영역을 채울 수 없음
// const long long MOD = 1000000007;  // 결과의 나머지 기준 선언
// long long previous = 1, current = 3;  // 너비 0과 2의 타일링 수 초기화
// for (int width = 4; width <= n; width += 2) {  // 짝수 너비의 점화식을 순서대로 적용
// long long next = (4 * current - previous + MOD) % MOD;  // 이전 두 짝수 너비로 다음 경우의 수 계산
// previous = current; current = next;  // 다음 너비 계산에 쓸 두 값 갱신
// }  // 블록 끝
// return (int)current;  // 3×n 타일링 수의 나머지 반환
// }  // 블록 끝

// 풀이 요약
// 짝수 너비에서 앞선 두 짝수 너비의 경우의 수를 4배와 뺄셈으로 연결하는 점화식 적용
```

## 채점 기록

- 언어: C++
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:45:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12902_3_x_n_%ED%83%80%EC%9D%BC%EB%A7%81/README.md)
