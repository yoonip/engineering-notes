# 중복된 숫자 개수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120583) · Level 0 · C

## 풀이

배열의 모든 원소를 순회하며 n과 같을 때마다 개수 증가. 중복된 원소도 등장한 횟수만큼 모두 셈.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len, int n) {
    int count = 0;
    for (size_t i = 0; i < array_len; ++i) count += array[i] == n;
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int array[], size_t array_len, int n) {  // 중복된 숫자 개수 풀이 시작
//     int count = 0;  // 찾을 값 n의 등장 횟수를 0으로 시작
//     for (size_t i = 0; i < array_len; ++i) count += array[i] == n;  // 배열을 모두 읽으며 원소가 n과 같을 때마다 개수 증가
//     return count;  // 중복 등장을 각각 포함한 n의 총 출현 횟수 반환
// }  // 블록 끝
// 풀이 요약
// 배열의 모든 원소를 순회하며 n과 같을 때마다 개수 증가. 중복된 원소도 등장한 횟수만큼 모두 셈.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120583_%EC%A4%91%EB%B3%B5%EB%90%9C_%EC%88%AB%EC%9E%90_%EA%B0%9C%EC%88%98/README.md)
