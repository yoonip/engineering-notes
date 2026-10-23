# n 번째 원소까지

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181889) · Level 0 · C

## 풀이

원본 배열의 앞 n개 원소를 새 배열에 복사.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int num_list[], size_t num_list_len, int n) {
    int* answer = malloc(n * sizeof(int));
    memcpy(answer, num_list, n * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int num_list[], size_t num_list_len, int n) {  // n 번째 원소까지 풀이 시작
//     int* answer = malloc(n * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, num_list, n * sizeof(int));  // 입력 배열의 앞 n개 원소를 새 결과 배열에 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 원본 배열의 앞 n개 원소를 새 배열에 복사.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:12:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181889_n_%EB%B2%88%EC%A7%B8_%EC%9B%90%EC%86%8C%EA%B9%8C%EC%A7%80/README.md)
