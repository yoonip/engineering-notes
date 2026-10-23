# 대충 만든 자판

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/160586) · Level 1 · C

## 풀이

알파벳마다 필요한 최소 누름 횟수를 계산; 목표 문자열의 횟수를 더하고 입력할 수 없는 문자가 있으면 -1을 반환

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

int* solution(const char* keymap[], size_t keymap_len, const char* targets[], size_t targets_len) {
    int presses[26]; for (int i = 0; i < 26; ++i) presses[i] = INT_MAX;
    for (size_t k = 0; k < keymap_len; ++k) for (size_t i = 0; keymap[k][i]; ++i) { int c = keymap[k][i] - 'A'; if ((int)i + 1 < presses[c]) presses[c] = (int)i + 1; }
    int* answer = malloc(targets_len * sizeof(int));
    for (size_t t = 0; t < targets_len; ++t) {
        int total = 0;
        for (size_t i = 0; targets[t][i]; ++i) { int count = presses[targets[t][i] - 'A']; if (count == INT_MAX) { total = -1; break; } total += count; }
        answer[t] = total;
    }
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
// int* solution(const char* keymap[], size_t keymap_len, const char* targets[], size_t targets_len) {  // 알파벳마다 필요한 최소 누름 횟수를 계산; 목표 문자열의 횟수를 더하고 입력할 수 없는 문자가 있으면 -1을 반환
//     int presses[26]; for (int i = 0; i < 26; ++i) presses[i] = INT_MAX;  // 키 또는 목표 단어의 문자 위치 / 알파벳별 최소 누름 횟수 저장
//     for (size_t k = 0; k < keymap_len; ++k) for (size_t i = 0; keymap[k][i]; ++i) { int c = keymap[k][i] - 'A'; if ((int)i + 1 < presses[c]) presses[c] = (int)i + 1; }  // 키맵의 키 번호 순서대로 확인; 키 또는 목표 단어의 문자 위치 갱신
//     int* answer = malloc(targets_len * sizeof(int));  // 목표별 최소 누름 횟수 공간 확보
//     for (size_t t = 0; t < targets_len; ++t) {  // 목표 단어 번호 순서대로 확인
//         int total = 0;  // 현재 목표를 쓰는 총 누름 횟수 저장
//         for (size_t i = 0; targets[t][i]; ++i) { int count = presses[targets[t][i] - 'A']; if (count == INT_MAX) { total = -1; break; } total += count; }  // 키 또는 목표 단어의 문자 위치 순서대로 확인; 현재 글자에 필요한 최소 횟수 / 현재 목표를 쓰는 총 누름 횟수 저장
//         answer[t] = total;  // 목표별 최소 누름 횟수 갱신
//     }  // 이 범위 끝
//     return answer;  // 목표별 최소 누름 횟수 반환
// }  // 이 범위 끝

// 풀이 요약
// 알파벳마다 필요한 최소 누름 횟수를 계산; 목표 문자열의 횟수를 더하고 입력할 수 없는 문자가 있으면 -1을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:47:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_160586_%EB%8C%80%EC%B6%A9_%EB%A7%8C%EB%93%A0_%EC%9E%90%ED%8C%90/README.md)
