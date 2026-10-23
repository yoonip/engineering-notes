# 정수 찾기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181840) · Level 0 · C

## 풀이

배열을 앞에서부터 순회해 정수 n과 같은 원소가 하나라도 있는지 확인.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int num_list[], size_t num_list_len, int n) {
    for (size_t i = 0; i < num_list_len; ++i) if (num_list[i] == n) return 1;
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int num_list[], size_t num_list_len, int n) {  // 정수 찾기 풀이 시작
//     for (size_t i = 0; i < num_list_len; ++i) if (num_list[i] == n) return 1;  // 배열에서 n과 같은 원소를 처음 찾으면 1 반환
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝
// 풀이 요약
// 배열을 앞에서부터 순회해 정수 n과 같은 원소가 하나라도 있는지 확인.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:24:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181840_%EC%A0%95%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
