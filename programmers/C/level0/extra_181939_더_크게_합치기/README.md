# 더 크게 합치기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181939) · Level 0 · C

## 풀이

두 정수를 두 순서로 이어 붙이고 더 큰 값을 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
int solution(int a, int b) {
    int scale_a = 10, scale_b = 10;
    while (scale_a <= a) scale_a *= 10;
    while (scale_b <= b) scale_b *= 10;
    int ab = a * scale_b + b, ba = b * scale_a + a;
    return ab > ba ? ab : ba;
}

// 전체 코드 줄별 설명
// int solution(int a, int b) {  // 더 크게 합치기 풀이 시작
//     int scale_a = 10, scale_b = 10;  // 각 정수를 이어 붙일 때 사용할 자릿수 배율을 10으로 초기화
//     while (scale_a <= a) scale_a *= 10;  // while과 *=로 a를 뒤에 붙일 때 필요한 자릿수 배율을 구하기
//     while (scale_b <= b) scale_b *= 10;  // while과 *=로 b를 뒤에 붙일 때 필요한 자릿수 배율을 구하기
//     int ab = a * scale_b + b, ba = b * scale_a + a;  // 자릿수 배율을 곱해 두 순서로 이어 붙인 수를 계산
//     return ab > ba ? ab : ba;  // 삼항 연산자 ?:로 두 연결 결과 중 큰 값을 반환
// }  // 블록 끝

// 풀이 요약
// 두 정수를 두 순서로 이어 붙이고 더 큰 값을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:28:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181939_%EB%8D%94_%ED%81%AC%EA%B2%8C_%ED%95%A9%EC%B9%98%EA%B8%B0/README.md)
