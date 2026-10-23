# 두 수의 연산값 비교하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181938) · Level 0 · C

## 풀이

a와 b를 이어 붙인 수와 2ab를 계산한 뒤 큰 값을 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
int solution(int a, int b) {
    int scale = 10;
    while (scale <= b) scale *= 10;
    int joined = a * scale + b, product = 2 * a * b;
    return joined > product ? joined : product;
}

// 전체 코드 줄별 설명
// int solution(int a, int b) {  // 두 수의 연산값 비교하기 풀이 시작
//     int scale = 10;  // 한 자리 수를 이어 붙일 때의 배율 10으로 초기화
//     while (scale <= b) scale *= 10;  // while과 *=로 b의 자릿수에 맞는 10의 거듭제곱을 구하기
//     int joined = a * scale + b, product = 2 * a * b;  // 곱셈과 덧셈으로 이어 붙인 수와 2ab를 각각 계산
//     return joined > product ? joined : product;  // 삼항 연산자 ?:로 비교한 두 값 중 큰 값을 반환
// }  // 블록 끝

// 풀이 요약
// a와 b를 이어 붙인 수와 2ab를 계산한 뒤 큰 값을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:28:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181938_%EB%91%90_%EC%88%98%EC%9D%98_%EC%97%B0%EC%82%B0%EA%B0%92_%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0/README.md)
