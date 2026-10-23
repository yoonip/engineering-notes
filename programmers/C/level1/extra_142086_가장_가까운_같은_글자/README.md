# 가장 가까운 같은 글자

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/142086) · Level 1 · C

## 풀이

문자마다 마지막 등장 위치를 저장; 처음 등장하면 -1, 다시 등장하면 현재 위치와 이전 위치의 차이를 기록

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

int* solution(const char* s) {
    int last[26]; for (int c = 0; c < 26; ++c) last[c] = -1;
    size_t n = strlen(s); int* answer = malloc(n * sizeof(int));
    for (size_t i = 0; i < n; ++i) { int c = s[i] - 'a'; answer[i] = last[c] < 0 ? -1 : (int)i - last[c]; last[c] = (int)i; }
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
// int* solution(const char* s) {  // 문자마다 마지막 등장 위치를 저장; 처음 등장하면 -1, 다시 등장하면 현재 위치와 이전 위치의 차이를 기록
//     int last[26]; for (int c = 0; c < 26; ++c) last[c] = -1;  // 모든 알파벳을 아직 나오지 않은 위치 -1로 초기화
//     size_t n = strlen(s); int* answer = malloc(n * sizeof(int));  // 문자열 길이 / 가장 가까운 같은 문자까지의 거리 공간 확보
//     for (size_t i = 0; i < n; ++i) { int c = s[i] - 'a'; answer[i] = last[c] < 0 ? -1 : (int)i - last[c]; last[c] = (int)i; }  // 현재 문자 위치 순서대로 확인; 현재 알파벳 번호 / 가장 가까운 같은 문자까지의 거리 / 알파벳이 마지막으로 나온 위치 저장
//     return answer;  // 가장 가까운 같은 문자까지의 거리 반환
// }  // 이 범위 끝

// 풀이 요약
// 문자마다 마지막 등장 위치를 저장; 처음 등장하면 -1, 다시 등장하면 현재 위치와 이전 위치의 차이를 기록
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:48:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_142086_%EA%B0%80%EC%9E%A5_%EA%B0%80%EA%B9%8C%EC%9A%B4_%EA%B0%99%EC%9D%80_%EA%B8%80%EC%9E%90/README.md)
