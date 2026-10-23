# 피로도

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/87946) · Level 2 · C

## 풀이

던전이 최대 8개이므로 모든 방문 순서를 확인; 입장 조건을 만족하는 동안 피로도를 차감해 방문 수를 세기
예: 80에서 80/20→30/10→50/40 순으로 세 곳 방문 가능.; 던전 N개일 때 시간 O(N!*N), 순열 작업 공간 O(N)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int search(int fatigue, int** dungeons, size_t count, unsigned used) {
    int best = 0;
    for (size_t i = 0; i < count; ++i) if (!(used & (1u << i)) && fatigue >= dungeons[i][0]) {
        int value = 1 + search(fatigue - dungeons[i][1], dungeons, count, used | (1u << i));
        if (value > best) best = value;
    }
    return best;
}
int solution(int k, int** dungeons, size_t dungeons_rows, size_t dungeons_cols) {
    (void)dungeons_cols;
    return search(k, dungeons, dungeons_rows, 0);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static int search(int fatigue, int** dungeons, size_t count, unsigned used) {  // 지금 남은 피로도 / 던전 개수 / 이미 탐험한 던전 비트 계산용 함수
//     int best = 0;  // 앞으로 갈 수 있는 최대 던전 수 저장
//     for (size_t i = 0; i < count; ++i) if (!(used & (1u << i)) && fatigue >= dungeons[i][0]) {  // 방문하지 않았고 최소 피로도를 충족하는 던전만 선택
//         int value = 1 + search(fatigue - dungeons[i][1], dungeons, count, used | (1u << i));  // 던전 하나를 방문하고 소모 피로도를 뺀 뒤 더 갈 수 있는 최대 개수 계산
//         if (value > best) best = value;  // 이번 선택이 지금까지의 최댓값보다 크면 앞으로 갈 수 있는 최대 던전 수 갱신
//     }  // 이 범위 끝
//     return best;  // 앞으로 갈 수 있는 최대 던전 수 반환
// }  // 이 범위 끝
// int solution(int k, int** dungeons, size_t dungeons_rows, size_t dungeons_cols) {  // 던전이 최대 8개이므로 모든 방문 순서를 확인; 입장 조건을 만족하는 동안 피로도를 차감해 방문 수를 세기
//     (void)dungeons_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     return search(k, dungeons, dungeons_rows, 0);  // 아직 방문한 던전 없이 피로도 k에서 최대 방문 수 탐색
// }  // 이 범위 끝

// 풀이 요약
// 던전이 최대 8개이므로 모든 방문 순서를 확인; 입장 조건을 만족하는 동안 피로도를 차감해 방문 수를 세기
// 예: 80에서 80/20→30/10→50/40 순으로 세 곳 방문 가능.; 던전 N개일 때 시간 O(N!*N), 순열 작업 공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/047_87946_%ED%94%BC%EB%A1%9C%EB%8F%84/README.md)
