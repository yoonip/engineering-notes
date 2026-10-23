# 공배수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181936) · Level 0 · C

## 풀이

number가 n과 m 모두로 나누어떨어지는지 확인

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
int solution(int number, int n, int m) {
    return number % n == 0 && number % m == 0;
}

// 전체 코드 줄별 설명
// int solution(int number, int n, int m) {  // 공배수 풀이 시작
//     return number % n == 0 && number % m == 0;  // %와 ==로 두 배수 조건을 검사하고 &&로 모두 참인지 확인
// }  // 블록 끝

// 풀이 요약
// number가 n과 m 모두로 나누어떨어지는지 확인
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:29:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181936_%EA%B3%B5%EB%B0%B0%EC%88%98/README.md)
