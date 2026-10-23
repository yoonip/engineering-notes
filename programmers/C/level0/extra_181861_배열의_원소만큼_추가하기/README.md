# 배열의 원소만큼 추가하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181861) · Level 0 · C

## 풀이

각 수 a를 a번 반복한 묶음을 입력 순서대로 연결

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    size_t length = 0;
    for (size_t i = 0; i < arr_len; ++i) length += arr[i];
    int* answer = malloc(length * sizeof(int));
    size_t out = 0;
    for (size_t i = 0; i < arr_len; ++i) for (int j = 0; j < arr[i]; ++j) answer[out++] = arr[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 배열의 원소만큼 추가하기 풀이 시작
//     size_t length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < arr_len; ++i) length += arr[i];  // 각 값만큼 반복할 총 원소 수를 합산해 결과 길이 계산
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; i < arr_len; ++i) for (int j = 0; j < arr[i]; ++j) answer[out++] = arr[i];  // 각 원소의 값만큼 그 원소를 반복해 결과에 넣기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 수 a를 a번 반복한 묶음을 입력 순서대로 연결
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181861_%EB%B0%B0%EC%97%B4%EC%9D%98_%EC%9B%90%EC%86%8C%EB%A7%8C%ED%81%BC_%EC%B6%94%EA%B0%80%ED%95%98%EA%B8%B0/README.md)
