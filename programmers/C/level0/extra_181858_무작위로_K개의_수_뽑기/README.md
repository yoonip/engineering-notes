# 무작위로 K개의 수 뽑기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181858) · Level 0 · C

## 풀이

입력 순서대로 처음 등장한 서로 다른 수를 k개까지 남기고, 부족한 자리는 -1로 채움.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int k) {
    int* answer = malloc(k * sizeof(int));
    bool* seen = calloc(100001, sizeof(bool));
    int length = 0;
    for (size_t i = 0; i < arr_len && length < k; ++i) if (!seen[arr[i]]) {
        seen[arr[i]] = true;
        answer[length++] = arr[i];
    }
    while (length < k) answer[length++] = -1;
    free(seen);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int k) {  // 무작위로 K개의 수 뽑기 풀이 시작
//     int* answer = malloc(k * sizeof(int));  // answer를 저장할 메모리 확보
//     bool* seen = calloc(100001, sizeof(bool));  // seen에 쓸 메모리를 0으로 채워 확보
//     int length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < arr_len && length < k; ++i) if (!seen[arr[i]]) {  // 입력 순서대로 처음 보는 값만 고르기. 서로 다른 값 k개를 모으면 종료
//         seen[arr[i]] = true;  // 현재 값을 이미 선택한 값으로 표시
//         answer[length++] = arr[i];  // 처음 본 값을 결과에 저장하고 선택한 원소 수 증가
//     }  // 블록 끝
//     while (length < k) answer[length++] = -1;  // 서로 다른 수가 k개보다 적으면 부족한 자리를 -1로 채움
//     free(seen);  // free로 반환 결과에 사용하지 않는 임시 메모리를 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 입력 순서대로 처음 등장한 서로 다른 수를 k개까지 남기고, 부족한 자리는 -1로 채움.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:16:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181858_%EB%AC%B4%EC%9E%91%EC%9C%84%EB%A1%9C_K%EA%B0%9C%EC%9D%98_%EC%88%98_%EB%BD%91%EA%B8%B0/README.md)
