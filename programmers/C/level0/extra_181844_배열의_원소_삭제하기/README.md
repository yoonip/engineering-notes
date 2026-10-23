# 배열의 원소 삭제하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181844) · Level 0 · C

## 풀이

삭제 대상 집합에 없는 원소만 원래 순서대로 남기기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int delete_list[], size_t delete_list_len) {
    bool removed[1001] = {false};
    for (size_t i = 0; i < delete_list_len; ++i) removed[delete_list[i]] = true;
    size_t length = 0;
    for (size_t i = 0; i < arr_len; ++i) if (!removed[arr[i]]) ++length;
    int* answer = malloc(length * sizeof(int));
    size_t out = 0;
    for (size_t i = 0; i < arr_len; ++i) if (!removed[arr[i]]) answer[out++] = arr[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int delete_list[], size_t delete_list_len) {  // 배열의 원소 삭제하기 풀이 시작
//     bool removed[1001] = {false};  // 삭제 대상인지 표시한 집합 저장
//     for (size_t i = 0; i < delete_list_len; ++i) removed[delete_list[i]] = true;  // 삭제 목록의 각 값을 삭제 대상 표시 배열에 기록
//     size_t length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < arr_len; ++i) if (!removed[arr[i]]) ++length;  // 지울 값으로 표시되지 않은 원소 수를 먼저 세기
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; i < arr_len; ++i) if (!removed[arr[i]]) answer[out++] = arr[i];  // 삭제 대상이 아닌 값만 원래 순서대로 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 삭제 대상 집합에 없는 원소만 원래 순서대로 남기기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:41
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181844_%EB%B0%B0%EC%97%B4%EC%9D%98_%EC%9B%90%EC%86%8C_%EC%82%AD%EC%A0%9C%ED%95%98%EA%B8%B0/README.md)
