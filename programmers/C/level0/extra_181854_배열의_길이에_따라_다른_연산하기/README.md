# 배열의 길이에 따라 다른 연산하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181854) · Level 0 · C

## 풀이

원본을 복사한 뒤 길이가 홀수이면 짝수 인덱스 0, 2, 4, …에 n을 더하기. 길이가 짝수이면 홀수 인덱스 1, 3, 5, …에 n을 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int n) {
    int* answer = malloc(arr_len * sizeof(int));
    memcpy(answer, arr, arr_len * sizeof(int));
    for (size_t i = arr_len % 2 ? 0 : 1; i < arr_len; i += 2) answer[i] += n;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int n) {  // 배열의 길이에 따라 다른 연산하기 풀이 시작
//     int* answer = malloc(arr_len * sizeof(int));  // malloc으로 원래 배열과 같은 개수의 int를 저장할 answer 공간을 할당
//     memcpy(answer, arr, arr_len * sizeof(int));  // memcpy로 원래 원소를 answer에 모두 복사
//     for (size_t i = arr_len % 2 ? 0 : 1; i < arr_len; i += 2) answer[i] += n;  // 길이가 홀수이면 0, 짝수이면 1에서 시작해 인덱스를 2씩 늘리며 해당 원소에 n을 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 원본을 복사한 뒤 길이가 홀수이면 짝수 인덱스 0, 2, 4, …에 n을 더하기. 길이가 짝수이면 홀수 인덱스 1, 3, 5, …에 n을 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:18:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181854_%EB%B0%B0%EC%97%B4%EC%9D%98_%EA%B8%B8%EC%9D%B4%EC%97%90_%EB%94%B0%EB%9D%BC_%EB%8B%A4%EB%A5%B8_%EC%97%B0%EC%82%B0%ED%95%98%EA%B8%B0/README.md)
