# 숫자 변환하기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/154538) · Level 2 · C

## 풀이

연산이 항상 수를 키우므로 x부터 y까지 순서대로 최소 연산 횟수 갱신; 도달한 수에서 더하기 n, 2배, 3배를 적용하고 y를 넘는 값 제외
예: 10→20→40은 2회, 2에서 5는 n=4로 만들 수 없어 -1.; 시간·공간 O(y)

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

int solution(int x, int y, int n) {
    int* distance = malloc(((size_t)y + 1) * sizeof(*distance));
    for (int i = 0; i <= y; ++i) distance[i] = -1;
    distance[x] = 0;
    for (int value = x; value <= y; ++value) if (distance[value] >= 0) {
        int next[3] = {value + n, value * 2, value * 3};
        for (int j = 0; j < 3; ++j) if (next[j] <= y && (distance[next[j]] < 0 || distance[next[j]] > distance[value] + 1)) distance[next[j]] = distance[value] + 1;
    }
    int answer = distance[y]; free(distance);
    return answer;
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
// int solution(int x, int y, int n) {  // 연산이 항상 수를 키우므로 x부터 y까지 순서대로 최소 연산 횟수 갱신; 도달한 수에서 더하기 n, 2배, 3배를 적용하고 y를 넘는 값 제외
//     int* distance = malloc(((size_t)y + 1) * sizeof(*distance));  // 정수별 최소 연산 횟수 공간 확보
//     for (int i = 0; i <= y; ++i) distance[i] = -1;  // 거리 배열 초기화 위치 순서대로 확인; 정수별 최소 연산 횟수 갱신
//     distance[x] = 0;  // 정수별 최소 연산 횟수 갱신
//     for (int value = x; value <= y; ++value) if (distance[value] >= 0) {  // 이미 도달한 정수에서만 다음 덧셈과 곱셈 상태로 확장
//         int next[3] = {value + n, value * 2, value * 3};  // 더하기 두 배 세 배의 다음 후보 저장
//         for (int j = 0; j < 3; ++j) if (next[j] <= y && (distance[next[j]] < 0 || distance[next[j]] > distance[value] + 1)) distance[next[j]] = distance[value] + 1;  // 다음 연산 종류 순서대로 확인; 이번 경로가 저장된 최단 거리보다 짧으면 정수별 최소 연산 횟수 / 더하기 두 배 세 배의 다음 후보 / 다음 연산 종류 / 연산을 확장할 정수 확인
//     }  // 이 범위 끝
//     int answer = distance[y]; free(distance);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // y까지의 최소 연산 횟수 반환
// }  // 이 범위 끝

// 풀이 요약
// 연산이 항상 수를 키우므로 x부터 y까지 순서대로 최소 연산 횟수 갱신; 도달한 수에서 더하기 n, 2배, 3배를 적용하고 y를 넘는 값 제외
// 예: 10→20→40은 2회, 2에서 5는 n=4로 만들 수 없어 -1.; 시간·공간 O(y)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/026_154538_%EC%88%AB%EC%9E%90_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0/README.md)
