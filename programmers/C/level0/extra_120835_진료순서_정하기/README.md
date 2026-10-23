# 진료순서 정하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120835) · Level 0 · C

## 풀이

각 환자보다 응급도가 큰 환자 수에 1을 더해 순위 계산. 입력 위치별로 따로 계산하므로 결과 순서는 원본과 같음.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int emergency[], size_t emergency_len) {
    int* answer = malloc(emergency_len * sizeof(*answer));
    for (size_t i = 0; i < emergency_len; ++i) {
        answer[i] = 1;
        for (size_t j = 0; j < emergency_len; ++j) answer[i] += emergency[j] > emergency[i];
    }
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
// int* solution(int emergency[], size_t emergency_len) {  // 진료순서 정하기 풀이 시작
//     int* answer = malloc(emergency_len * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < emergency_len; ++i) {  // 각 환자의 진료 순위를 따로 계산
//         answer[i] = 1;  // 자기 등수는 1부터 시작. 더 큰 값이 나올 때마다 1씩 밀리게 계산
//         for (size_t j = 0; j < emergency_len; ++j) answer[i] += emergency[j] > emergency[i];  // 응급도가 현재 환자보다 높은 환자마다 등수에 1 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 환자보다 응급도가 큰 환자 수에 1을 더해 순위 계산. 입력 위치별로 따로 계산하므로 결과 순서는 원본과 같음.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:25
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120835_%EC%A7%84%EB%A3%8C%EC%88%9C%EC%84%9C_%EC%A0%95%ED%95%98%EA%B8%B0/README.md)
