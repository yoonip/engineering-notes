# n의 배수 고르기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120905) · Level 0 · C

## 풀이

입력 배열을 앞에서부터 읽으며 n으로 나눈 나머지가 0인 원소만 결과 배열에 저장. 입력에서의 원소 순서를 유지

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int n, int numlist[], size_t numlist_len) {
    int* answer = malloc((numlist_len ? numlist_len : 1) * sizeof(*answer));
    size_t pos = 0;
    for (size_t i = 0; i < numlist_len; ++i) if (numlist[i] % n == 0) answer[pos++] = numlist[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int* solution(int n, int numlist[], size_t numlist_len) {  // n의 배수 고르기 풀이 시작
//     int* answer = malloc((numlist_len ? numlist_len : 1) * sizeof(*answer));  // 모든 입력 원소가 n의 배수인 경우까지 담도록 numlist_len개 정수 공간을 확보하며, 길이가 0이면 최소 한 칸을 확보
//     size_t pos = 0;  // size_t 변수 pos는 지금까지 고른 배수의 개수이자 다음 결과를 쓸 인덱스이며, 처음에는 0임
//     for (size_t i = 0; i < numlist_len; ++i) if (numlist[i] % n == 0) answer[pos++] = numlist[i];  // for로 입력 순서를 유지하며 순회. % n의 나머지가 0인 원소만 answer[pos]에 저장하고 후위 증가 pos++로 다음 저장 위치를 준비
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 배열을 앞에서부터 읽으며 n으로 나눈 나머지가 0인 원소만 결과 배열에 저장. 입력에서의 원소 순서를 유지
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:25:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120905_n%EC%9D%98_%EB%B0%B0%EC%88%98_%EA%B3%A0%EB%A5%B4%EA%B8%B0/README.md)
