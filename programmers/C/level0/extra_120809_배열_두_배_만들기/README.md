# 배열 두 배 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120809) · Level 0 · C

## 풀이

원소 순서를 유지하며 각 값을 두 배로 바꾸기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int numbers[], size_t numbers_len) {
    int* answer = malloc(numbers_len * sizeof(*answer));
    for (size_t i = 0; i < numbers_len; ++i) answer[i] = 2 * numbers[i];
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
// int* solution(int numbers[], size_t numbers_len) {  // 배열 두 배 만들기 풀이 시작
//     int* answer = malloc(numbers_len * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < numbers_len; ++i) answer[i] = 2 * numbers[i];  // 각 입력 원소를 두 배로 계산해 같은 인덱스의 결과에 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 원소 순서를 유지하며 각 값을 두 배로 바꾸기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:54:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120809_%EB%B0%B0%EC%97%B4_%EB%91%90_%EB%B0%B0_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
