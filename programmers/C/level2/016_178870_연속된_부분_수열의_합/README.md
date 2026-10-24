# 연속된 부분 수열의 합

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/178870) · Level 2 · C

## 풀이

양수 수열이므로 오른쪽을 늘리면 합이 증가하고 왼쪽을 줄이면 감소하기; 두 포인터로 합 k인 최소 길이 구간을 찾기

예: [1,2,3,4,5],k=7은 [3,4]의 인덱스 [2,3]; 같은 길이는 먼저 찾은 답을 유지; 시간 O(N), 공간 O(1)

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

int* solution(int sequence[], size_t sequence_len, int k) {
    int* answer = malloc(2 * sizeof(*answer)); answer[0] = 0; answer[1] = (int)sequence_len;
    size_t left = 0; long long total = 0;
    for (size_t right = 0; right < sequence_len; ++right) {
        total += sequence[right];
        while (total > k) total -= sequence[left++];
        if (total == k && (int)(right - left) < answer[1] - answer[0]) { answer[0] = (int)left; answer[1] = (int)right; }
    }
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
// int* solution(int sequence[], size_t sequence_len, int k) {  // 양수 수열이므로 오른쪽을 늘리면 합이 증가하고 왼쪽을 줄이면 감소하기; 두 포인터로 합 k인 최소 길이 구간을 찾기
//     int* answer = malloc(2 * sizeof(*answer)); answer[0] = 0; answer[1] = (int)sequence_len;  // 가장 짧고 빠른 합 k 구간 공간 확보
//     size_t left = 0; long long total = 0;  // 현재 구간 왼쪽 / 현재 구간의 합 저장
//     for (size_t right = 0; right < sequence_len; ++right) {  // 현재 구간 오른쪽 순서대로 확인
//         total += sequence[right];  // 현재 구간의 합 / 현재 구간 오른쪽 더해 누적
//         while (total > k) total -= sequence[left++];  // 구간 합이 k를 넘는 동안 왼쪽 원소를 빼서 구간 줄이기
//         if (total == k && (int)(right - left) < answer[1] - answer[0]) { answer[0] = (int)left; answer[1] = (int)right; }  // 합이 k이고 기존 답보다 짧은 구간이면 가장 짧고 빠른 합 k 구간 갱신
//     }  // 이 범위 끝
//     return answer;  // 가장 짧고 빠른 합 k 구간 반환
// }  // 이 범위 끝

// 풀이 요약
// 양수 수열이므로 오른쪽을 늘리면 합이 증가하고 왼쪽을 줄이면 감소하기; 두 포인터로 합 k인 최소 길이 구간을 찾기
// 예: [1,2,3,4,5],k=7은 [3,4]의 인덱스 [2,3]; 같은 길이는 먼저 찾은 답을 유지; 시간 O(N), 공간 O(1)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:10:14
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/016_178870_%EC%97%B0%EC%86%8D%EB%90%9C_%EB%B6%80%EB%B6%84_%EC%88%98%EC%97%B4%EC%9D%98_%ED%95%A9/README.md)
