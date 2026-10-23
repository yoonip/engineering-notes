# 두 큐 합 같게 만들기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/118667) · Level 2 · C

## 풀이

합이 큰 큐의 앞 원소를 작은 큐로 옮기기; 양수이므로 목표보다 큰 구간은 앞을 줄이고 작으면 뒤를 늘리는 두 포인터와 같음
예: 첫 예제는 3을 옮긴 뒤 4를 받아 2회.; 같은 길이 N인 큐에서 시간·공간 O(N)

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

int solution(int queue1[], size_t queue1_len, int queue2[], size_t queue2_len) {
    size_t length = queue1_len + queue2_len, left = 0, right = queue1_len;
    int* circle = malloc(length * sizeof(*circle)); long long current = 0, total = 0;
    for (size_t i = 0; i < queue1_len; ++i) { circle[i] = queue1[i]; current += queue1[i]; }
    for (size_t i = 0; i < queue2_len; ++i) circle[queue1_len + i] = queue2[i];
    for (size_t i = 0; i < length; ++i) total += circle[i];
    if (total % 2) { free(circle); return -1; }
    long long target = total / 2;
    for (size_t moves = 0; moves <= 2 * length; ++moves) {
        if (current == target) { free(circle); return (int)moves; }
        if (current > target) current -= circle[left++ % length];
        else current += circle[right++ % length];
    }
    free(circle);
    return -1;
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
// int solution(int queue1[], size_t queue1_len, int queue2[], size_t queue2_len) {  // 합이 큰 큐의 앞 원소를 작은 큐로 옮기기; 양수이므로 목표보다 큰 구간은 앞을 줄이고 작으면 뒤를 늘리는 두 포인터와 같음
//     size_t length = queue1_len + queue2_len, left = 0, right = queue1_len;  // 두 큐 전체 길이 / 첫 큐에서 뺄 위치 / 둘째 큐에서 가져올 위치 저장
//     int* circle = malloc(length * sizeof(*circle)); long long current = 0, total = 0;  // 두 큐를 이어 붙인 원형 배열 / 현재 첫 큐 합 / 두 큐 전체 합 공간 확보
//     for (size_t i = 0; i < queue1_len; ++i) { circle[i] = queue1[i]; current += queue1[i]; }  // 큐 원소 복사 위치 순서대로 확인; 두 큐를 이어 붙인 원형 배열 갱신
//     for (size_t i = 0; i < queue2_len; ++i) circle[queue1_len + i] = queue2[i];  // 큐 원소 복사 위치 순서대로 확인; 두 큐를 이어 붙인 원형 배열 갱신
//     for (size_t i = 0; i < length; ++i) total += circle[i];  // 큐 원소 복사 위치 순서대로 확인; 두 큐 전체 합 / 두 큐를 이어 붙인 원형 배열 / 큐 원소 복사 위치 더해 누적
//     if (total % 2) { free(circle); return -1; }  // 전체 합이 홀수라 같은 두 합으로 나눌 수 없으면 두 큐를 이어 붙인 원형 배열 임시 공간 정리
//     long long target = total / 2;  // 각 큐가 가져야 할 합 저장
//     for (size_t moves = 0; moves <= 2 * length; ++moves) {  // 원소를 옮긴 횟수 순서대로 확인
//         if (current == target) { free(circle); return (int)moves; }  // 첫 큐 합이 목표 합과 같아졌으면 두 큐를 이어 붙인 원형 배열 / 원소를 옮긴 횟수 임시 공간 정리
//         if (current > target) current -= circle[left++ % length];  // 첫 큐 합이 목표보다 크면 앞 원소를 빼서 둘째 큐로 넘기기
//         else current += circle[right++ % length];  // 앞 조건이 아니면 둘째 큐에서 가져올 위치 갱신
//     }  // 이 범위 끝
//     free(circle);  // 두 큐를 이어 붙인 원형 배열 임시 공간 정리
//     return -1;  // 조건에 맞는 답이 없으면 -1
// }  // 이 범위 끝

// 풀이 요약
// 합이 큰 큐의 앞 원소를 작은 큐로 옮기기; 양수이므로 목표보다 큰 구간은 앞을 줄이고 작으면 뒤를 늘리는 두 포인터와 같음
// 예: 첫 예제는 3을 옮긴 뒤 4를 받아 2회.; 같은 길이 N인 큐에서 시간·공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/043_118667_%EB%91%90_%ED%81%90_%ED%95%A9_%EA%B0%99%EA%B2%8C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
