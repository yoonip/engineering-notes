# 최댓값 만들기(1)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120847) · Level 0 · C

## 풀이

모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대임

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int numbers[], size_t numbers_len) {
    int first = -1, second = -1;
    for (size_t i = 0; i < numbers_len; ++i) {
        if (numbers[i] >= first) { second = first; first = numbers[i]; }
        else if (numbers[i] > second) second = numbers[i];
    }
    return first * second;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int numbers[], size_t numbers_len) {  // 최댓값 만들기(1) 풀이 시작
//     int first = -1, second = -1;  // 가장 큰 값과 두 번째로 큰 값. 입력은 음수가 없어서 -1로 시작
//     for (size_t i = 0; i < numbers_len; ++i) {  // 원소를 한 번씩 읽어 가장 큰 두 값 유지
//         if (numbers[i] >= first) { second = first; first = numbers[i]; }  // 새 최댓값이면 기존 최댓값을 두 번째 자리로 밀기
//         else if (numbers[i] > second) second = numbers[i];  // 최댓값은 아니지만 두 번째 값보다 크면 두 번째 최댓값 교체
//     }  // 블록 끝
//     return first * second;  // 가장 큰 두 원소의 곱 반환
// }  // 블록 끝
// 풀이 요약
// 모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대임
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120847_%EC%B5%9C%EB%8C%93%EA%B0%92_%EB%A7%8C%EB%93%A4%EA%B8%B0%281%29/README.md)
