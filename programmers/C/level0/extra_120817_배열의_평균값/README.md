# 배열의 평균값

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120817) · Level 0 · C

## 풀이

평균은 전체 합을 원소 개수로 나눈 값임

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

double solution(int numbers[], size_t numbers_len) {
    double sum = 0;
    for (size_t i = 0; i < numbers_len; ++i) sum += numbers[i];
    return sum / numbers_len;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// double solution(int numbers[], size_t numbers_len) {  // 배열의 평균값 풀이 시작
//     double sum = 0;  // 평균을 구할 합. 소수 부분을 남기려고 double 사용
//     for (size_t i = 0; i < numbers_len; ++i) sum += numbers[i];  // 배열의 모든 원소를 double 합에 더함
//     return sum / numbers_len;  // 실수 합을 원소 수로 나눠 평균 반환
// }  // 블록 끝
// 풀이 요약
// 평균은 전체 합을 원소 개수로 나눈 값임
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120817_%EB%B0%B0%EC%97%B4%EC%9D%98_%ED%8F%89%EA%B7%A0%EA%B0%92/README.md)
