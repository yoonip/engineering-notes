# 로또의 최고 순위와 최저 순위

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77484) · Level 1 · C

## 풀이

확정 일치 개수와 알아볼 수 없는 0의 개수를 세기; 0이 모두 맞는 경우와 모두 틀리는 경우의 순위를 계산

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int* solution(int lottos[], size_t lottos_len, int win_nums[], size_t win_nums_len) {
    int matched = 0, unknown = 0;
    for (size_t i = 0; i < lottos_len; ++i) {
        if (lottos[i] == 0) ++unknown;
        else for (size_t j = 0; j < win_nums_len; ++j) if (lottos[i] == win_nums[j]) { ++matched; break; }
    }
    int* answer = malloc(2 * sizeof(int));
    answer[0] = 7 - matched - unknown; if (answer[0] > 6) answer[0] = 6;
    answer[1] = 7 - matched; if (answer[1] > 6) answer[1] = 6;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int* solution(int lottos[], size_t lottos_len, int win_nums[], size_t win_nums_len) {  // 확정 일치 개수와 알아볼 수 없는 0의 개수를 세기; 0이 모두 맞는 경우와 모두 틀리는 경우의 순위를 계산
//     int matched = 0, unknown = 0;  // 확인된 당첨 번호 수 / 알아볼 수 없는 0의 개수 저장
//     for (size_t i = 0; i < lottos_len; ++i) {  // 구매 번호 위치 순서대로 확인
//         if (lottos[i] == 0) ++unknown;  // 0은 알 수 없는 번호이므로 최고 순위 계산용 개수에 추가
//         else for (size_t j = 0; j < win_nums_len; ++j) if (lottos[i] == win_nums[j]) { ++matched; break; }  // 0이 아닌 번호는 당첨 번호와 비교해서 맞힌 개수 늘리기
//     }  // 이 범위 끝
//     int* answer = malloc(2 * sizeof(int));  // 최고 순위와 최저 순위 공간 확보
//     answer[0] = 7 - matched - unknown; if (answer[0] > 6) answer[0] = 6;  // 최고 순위와 최저 순위 갱신
//     answer[1] = 7 - matched; if (answer[1] > 6) answer[1] = 6;  // 최고 순위와 최저 순위 갱신
//     return answer;  // 최고 순위와 최저 순위 반환
// }  // 이 범위 끝

// 풀이 요약
// 확정 일치 개수와 알아볼 수 없는 0의 개수를 세기; 0이 모두 맞는 경우와 모두 틀리는 경우의 순위를 계산
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:54:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_77484_%EB%A1%9C%EB%98%90%EC%9D%98_%EC%B5%9C%EA%B3%A0_%EC%88%9C%EC%9C%84%EC%99%80_%EC%B5%9C%EC%A0%80_%EC%88%9C%EC%9C%84/README.md)
