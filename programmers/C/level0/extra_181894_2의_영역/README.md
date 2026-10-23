# 2의 영역

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181894) · Level 0 · C

## 풀이

모든 2를 포함하려면 첫 2에서 마지막 2까지의 구간이 필요

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    int first = -1, last = -1;
    for (size_t i = 0; i < arr_len; ++i) if (arr[i] == 2) { if (first < 0) first = (int)i; last = (int)i; }
    int length = first < 0 ? 1 : last - first + 1;
    int* answer = malloc(length * sizeof(int));
    if (first < 0) answer[0] = -1;
    else memcpy(answer, arr + first, length * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 2의 영역 풀이 시작
//     int first = -1, last = -1;  // 숫자 2의 첫 위치와 마지막 위치를 미등장 표시 -1로 초기화
//     for (size_t i = 0; i < arr_len; ++i) if (arr[i] == 2) { if (first < 0) first = (int)i; last = (int)i; }  // 2가 처음 나온 위치와 마지막 위치를 함께 기록
//     int length = first < 0 ? 1 : last - first + 1;  // 결과의 원소 수 저장
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     if (first < 0) answer[0] = -1;  // 2가 한 번도 없으면 결과를 {-1}로 채움
//     else memcpy(answer, arr + first, length * sizeof(int));  // 첫 2부터 마지막 2까지 양 끝을 포함해 원본 구간 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 모든 2를 포함하려면 첫 2에서 마지막 2까지의 구간이 필요
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:04:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181894_2%EC%9D%98_%EC%98%81%EC%97%AD/README.md)
