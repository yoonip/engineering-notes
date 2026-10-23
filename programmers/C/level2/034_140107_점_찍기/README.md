# 점 찍기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/140107) · Level 2 · C

## 풀이

각 x에서 원 내부의 최대 y를 구하고, 0부터 그 y까지 k의 배수인 좌표 수를 더하기
예: k=2,d=4이면 x=0,2,4에서 각각 3,2,1개로 총 6개.; 시간 O(d/k+1), 공간 O(1)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static long long integer_sqrt(long long value) {
    long long root = (long long)sqrtl((long double)value);
    while ((root + 1) * (root + 1) <= value) ++root;
    while (root * root > value) --root;
    return root;
}
long long solution(int k, int d) {
    long long answer = 0;
    for (long long x = 0; x <= d; x += k) answer += integer_sqrt((long long)d * d - x * x) / k + 1;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static long long integer_sqrt(long long value) {  // 제곱근 근삿값을 정수 비교로 보정
//     long long root = (long long)sqrtl((long double)value);  // 제곱근의 정수 후보 저장
//     while ((root + 1) * (root + 1) <= value) ++root;  // 다음 정수도 제곱해서 value 이하이면 제곱근 후보 올리기
//     while (root * root > value) --root;  // 현재 제곱이 value를 넘으면 제곱근 후보 내리기
//     return root;  // 제곱근의 정수 후보 반환
// }  // 이 범위 끝
// long long solution(int k, int d) {  // 각 x에서 원 내부의 최대 y를 구하고, 0부터 그 y까지 k의 배수인 좌표 수를 더하기
//     long long answer = 0;  // 원 안의 격자점 수 저장
//     for (long long x = 0; x <= d; x += k) answer += integer_sqrt((long long)d * d - x * x) / k + 1;  // k 간격으로 고른 가로 좌표 순서대로 확인; 원 안의 격자점 수 / k 간격으로 고른 가로 좌표 더해 누적
//     return answer;  // 원 안의 격자점 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 x에서 원 내부의 최대 y를 구하고, 0부터 그 y까지 k의 배수인 좌표 수를 더하기
// 예: k=2,d=4이면 x=0,2,4에서 각각 3,2,1개로 총 6개.; 시간 O(d/k+1), 공간 O(1)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:15:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/034_140107_%EC%A0%90_%EC%B0%8D%EA%B8%B0/README.md)
