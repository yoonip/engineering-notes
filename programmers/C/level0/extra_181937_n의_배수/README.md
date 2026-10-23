# n의 배수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181937) · Level 0 · C

## 풀이

num을 n으로 나눈 나머지가 0인지 확인

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
int solution(int num, int n) {
    return num % n == 0;
}

// 전체 코드 줄별 설명
// int solution(int num, int n) {  // n의 배수 풀이 시작
//     return num % n == 0;  // %로 나머지를 구하고 ==로 0과 비교해 1 또는 0을 반환
// }  // 블록 끝

// 풀이 요약
// num을 n으로 나눈 나머지가 0인지 확인
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:29:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181937_n%EC%9D%98_%EB%B0%B0%EC%88%98/README.md)
