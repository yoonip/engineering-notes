# 조건에 맞게 수열 변환하기 3

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181835) · Level 0 · C

## 풀이

각 원소에 대해 k가 홀수이면 arr[i] * k를, 짝수이면 arr[i] + k를 계산하여 같은 위치의 새 배열에 저장

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int k) {
    int* answer = malloc(arr_len * sizeof(int));
    for (size_t i = 0; i < arr_len; ++i) answer[i] = k % 2 ? arr[i] * k : arr[i] + k;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int k) {  // 조건에 맞게 수열 변환하기 3 풀이 시작
//     int* answer = malloc(arr_len * sizeof(int));  // 입력 배열과 같은 개수의 int를 저장할 결과 공간을 malloc으로 할당
//     for (size_t i = 0; i < arr_len; ++i) answer[i] = k % 2 ? arr[i] * k : arr[i] + k;  // 각 원소를 순회하며 k % 2가 참이면 k를 곱하고, 거짓이면 k를 더한 값을 answer에 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 원소에 대해 k가 홀수이면 arr[i] * k를, 짝수이면 arr[i] + k를 계산하여 같은 위치의 새 배열에 저장
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:22:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181835_%EC%A1%B0%EA%B1%B4%EC%97%90_%EB%A7%9E%EA%B2%8C_%EC%88%98%EC%97%B4_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0_3/README.md)
