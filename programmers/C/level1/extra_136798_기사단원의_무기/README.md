# 기사단원의 무기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/136798) · Level 1 · C

## 풀이

각 수의 배수를 순회하며 약수의 개수를 누적하기; 약수 개수가 제한을 넘으면 정해진 공격력을 사용

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int number, int limit, int power) {
    int* counts = calloc(number + 1, sizeof(int));
    for (int divisor = 1; divisor <= number; ++divisor) for (int multiple = divisor; multiple <= number; multiple += divisor) ++counts[multiple];
    int answer = 0;
    for (int i = 1; i <= number; ++i) answer += counts[i] > limit ? power : counts[i];
    free(counts);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int solution(int number, int limit, int power) {  // 각 수의 배수를 순회하며 약수의 개수를 누적하기; 약수 개수가 제한을 넘으면 정해진 공격력을 사용
//     int* counts = calloc(number + 1, sizeof(int));  // 기사 번호별 약수 개수 공간 확보하고 0으로 시작
//     for (int divisor = 1; divisor <= number; ++divisor) for (int multiple = divisor; multiple <= number; multiple += divisor) ++counts[multiple];  // 약수 후보의 모든 배수에 약수 개수 1씩 추가
//     int answer = 0;  // 제한을 적용한 철의 총무게 저장
//     for (int i = 1; i <= number; ++i) answer += counts[i] > limit ? power : counts[i];  // 무게를 합할 기사 번호 순서대로 확인; 제한을 적용한 철의 총무게 / 기사 번호별 약수 개수 / 무게를 합할 기사 번호 더해 누적
//     free(counts);  // 기사 번호별 약수 개수 임시 공간 정리
//     return answer;  // 제한을 적용한 철의 총무게 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 수의 배수를 순회하며 약수의 개수를 누적하기; 약수 개수가 제한을 넘으면 정해진 공격력을 사용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:49:51
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_136798_%EA%B8%B0%EC%82%AC%EB%8B%A8%EC%9B%90%EC%9D%98_%EB%AC%B4%EA%B8%B0/README.md)
