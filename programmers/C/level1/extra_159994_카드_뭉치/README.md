# 카드 뭉치

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/159994) · Level 1 · C

## 풀이

각 카드 뭉치의 맨 앞 위치를 따로 관리하기; 목표 단어를 두 뭉치의 현재 맨 앞 중 하나에서만 꺼내기

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

static char* copy_text(const char* text) {
    char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;
}
char* solution(const char* cards1[], size_t cards1_len, const char* cards2[], size_t cards2_len, const char* goal[], size_t goal_len) {
    size_t i = 0, j = 0;
    for (size_t k = 0; k < goal_len; ++k) {
        if (i < cards1_len && strcmp(cards1[i], goal[k]) == 0) ++i;
        else if (j < cards2_len && strcmp(cards2[j], goal[k]) == 0) ++j;
        else return copy_text("No");
    }
    return copy_text("Yes");
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
// static char* copy_text(const char* text) {  // 문자열을 새 공간에 복사해서 돌려주기
//     char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;  // Yes 또는 No 문자열 사본 공간 확보
// }  // 이 범위 끝
// char* solution(const char* cards1[], size_t cards1_len, const char* cards2[], size_t cards2_len, const char* goal[], size_t goal_len) {  // 각 카드 뭉치의 맨 앞 위치를 따로 관리하기; 목표 단어를 두 뭉치의 현재 맨 앞 중 하나에서만 꺼내기
//     size_t i = 0, j = 0;  // 첫 카드 뭉치의 다음 위치 / 둘째 카드 뭉치의 다음 위치 저장
//     for (size_t k = 0; k < goal_len; ++k) {  // 만들어야 할 goal의 위치 순서대로 확인
//         if (i < cards1_len && strcmp(cards1[i], goal[k]) == 0) ++i;  // 찾는 이름 또는 앞부분 문자열이 같으면 첫 카드 뭉치의 다음 위치 갱신
//         else if (j < cards2_len && strcmp(cards2[j], goal[k]) == 0) ++j;  // 그 외에는 찾는 이름 또는 앞부분 문자열이 같으면 둘째 카드 뭉치의 다음 위치 갱신
//         else return copy_text("No");  // 두 뭉치 맨 앞에 목표 단어가 없으면 No
//     }  // 이 범위 끝
//     return copy_text("Yes");  // 목표 단어를 전부 꺼냈으면 Yes
// }  // 이 범위 끝

// 풀이 요약
// 각 카드 뭉치의 맨 앞 위치를 따로 관리하기; 목표 단어를 두 뭉치의 현재 맨 앞 중 하나에서만 꺼내기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:47:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_159994_%EC%B9%B4%EB%93%9C_%EB%AD%89%EC%B9%98/README.md)
