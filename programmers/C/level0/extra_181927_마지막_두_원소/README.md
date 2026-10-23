# 마지막 두 원소

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181927) · Level 0 · C

## 풀이

마지막 값이 직전 값보다 크면 차이를, 아니면 마지막 값의 두 배를 추가

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

int* solution(int num_list[], size_t num_list_len) {
    int* answer = malloc((num_list_len + 1) * sizeof(int));
    memcpy(answer, num_list, num_list_len * sizeof(int));
    int last = num_list[num_list_len - 1], previous = num_list[num_list_len - 2];
    answer[num_list_len] = last > previous ? last - previous : last * 2;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int* solution(int num_list[], size_t num_list_len) {  // 마지막 두 원소 풀이 시작
//     int* answer = malloc((num_list_len + 1) * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     memcpy(answer, num_list, num_list_len * sizeof(int));  // memcpy로 원래 정수 배열을 새 결과 배열의 앞부분에 복사
//     int last = num_list[num_list_len - 1], previous = num_list[num_list_len - 2];  // []로 마지막 원소와 직전 원소를 각각 저장
//     answer[num_list_len] = last > previous ? last - previous : last * 2;  // >와 삼항 연산자 ?:로 차이 또는 마지막 값의 두 배를 골라 뒤에 추가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 마지막 값이 직전 값보다 크면 차이를, 아니면 마지막 값의 두 배를 추가
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:40:03
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181927_%EB%A7%88%EC%A7%80%EB%A7%89_%EB%91%90_%EC%9B%90%EC%86%8C/README.md)
