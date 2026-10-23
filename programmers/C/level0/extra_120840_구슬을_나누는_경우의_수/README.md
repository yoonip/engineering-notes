# 구슬을 나누는 경우의 수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120840) · Level 0 · C

## 풀이

전체 balls개에서 share개를 고르는 조합을 구하기. 고르는 수와 남기는 수 중 작은 쪽으로 반복하고, 각 단계에서 조합의 곱셈·나눗셈 식을 누적

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int balls, int share) {
    if (share > balls - share) share = balls - share;
    long long answer = 1;
    for (int i = 1; i <= share; ++i) answer = answer * (balls - share + i) / i;
    return (int)answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int balls, int share) {  // 구슬을 나누는 경우의 수 풀이 시작
//     if (share > balls - share) share = balls - share;  // 조합의 대칭성으로 share와 balls - share 중 작은 값을 선택하여 곱셈·나눗셈 반복 횟수를 줄이기
//     long long answer = 1;  // 중간 곱을 담을 수 있도록 long long 변수 answer를 선언하고, 곱셈 누적의 시작값 1을 저장
//     for (int i = 1; i <= share; ++i) answer = answer * (balls - share + i) / i;  // i를 1부터 share까지 늘리며 answer에 balls - share + i를 곱하고 i로 나누어 조합 값을 단계적으로 계산
//     return (int)answer;  // 문제의 반환형에 맞게 최종 조합 값 answer를 int로 변환해 반환
// }  // 블록 끝

// 풀이 요약
// 전체 balls개에서 share개를 고르는 조합을 구하기. 고르는 수와 남기는 수 중 작은 쪽으로 반복하고, 각 단계에서 조합의 곱셈·나눗셈 식을 누적
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:32:06
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120840_%EA%B5%AC%EC%8A%AC%EC%9D%84_%EB%82%98%EB%88%84%EB%8A%94_%EA%B2%BD%EC%9A%B0%EC%9D%98_%EC%88%98/README.md)
