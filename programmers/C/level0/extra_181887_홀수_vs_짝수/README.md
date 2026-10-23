# 홀수 vs 짝수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181887) · Level 0 · C

## 풀이

원소의 값이 홀수인지가 아니라 원소의 순번이 홀수·짝수인지 구분

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int num_list[], size_t num_list_len) {
    int sums[2] = {0, 0};
    for (size_t i = 0; i < num_list_len; ++i) sums[i % 2] += num_list[i];
    return sums[0] > sums[1] ? sums[0] : sums[1];
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int num_list[], size_t num_list_len) {  // 홀수 vs 짝수 풀이 시작
//     int sums[2] = {0, 0};  // 홀수 번째와 짝수 번째 합계 저장
//     for (size_t i = 0; i < num_list_len; ++i) sums[i % 2] += num_list[i];  // i의 짝수·홀수에 따라 두 합을 따로 누적
//     return sums[0] > sums[1] ? sums[0] : sums[1];  // 홀수 번째 원소 합과 짝수 번째 원소 합 중 큰 값 반환
// }  // 블록 끝
// 풀이 요약
// 원소의 값이 홀수인지가 아니라 원소의 순번이 홀수·짝수인지 구분
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:12:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181887_%ED%99%80%EC%88%98_vs_%EC%A7%9D%EC%88%98/README.md)
