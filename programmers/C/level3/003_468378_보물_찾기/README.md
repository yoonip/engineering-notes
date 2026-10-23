# 보물 찾기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468378) · Level 3 · C

## 풀이

구간 DP로 현재 굴착 비용 + max(왼쪽 최악 비용, 오른쪽 최악 비용)을 최소화하는 열을 정하기
excavate의 방향 응답에 따라 그 전략의 왼쪽·오른쪽 구간으로 이동하기; 최소 최악 비용 이하로 항상 찾으므로 보장된 money를 넘지 않음; 시간 O(N³), 공간 O(N²)
예: 비용이 모두 1인 5열은 가운데를 먼저 파고, 응답 방향에서 같은 전략을 반복하면 최대 3번 안에 발굴하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

extern int excavate(int index);
int solution(int depth[], size_t depth_len, int money) {
    (void)money; size_t n = depth_len, stride = n + 1;
    int* dp = calloc(stride * stride, sizeof(*dp)); int* choice = calloc(stride * stride, sizeof(*choice));
    for (size_t size = 1; size <= n; ++size) for (size_t left = 0; left + size <= n; ++left) {
        size_t right = left + size; int best = INT_MAX;
        for (size_t middle = left; middle < right; ++middle) {
            int first = dp[left * stride + middle], second = dp[(middle + 1) * stride + right]; int cost = depth[middle] + (first > second ? first : second);
            if (cost < best) { best = cost; choice[left * stride + right] = (int)middle; }
        }
        dp[left * stride + right] = best;
    }
    size_t left = 0, right = n; int answer = 0;
    while (left < right) {
        size_t middle = (size_t)choice[left * stride + right]; int result = excavate((int)middle + 1);
        if (!result) { answer = (int)middle + 1; break; }
        if (result < 0) right = middle; else left = middle + 1;
    }
    free(dp); free(choice);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// extern int excavate(int index);  // 채점기가 제공하는 질의 함수
// int solution(int depth[], size_t depth_len, int money) {  // 구간 DP로 현재 굴착 비용 + max(왼쪽 최악 비용, 오른쪽 최악 비용)을 최소화하는 열을 정하기
//     (void)money; size_t n = depth_len, stride = n + 1;  // 발굴 위치 수 / 구간 DP 한 행 길이 갱신
//     int* dp = calloc(stride * stride, sizeof(*dp)); int* choice = calloc(stride * stride, sizeof(*choice));  // 탐색 구간별 최악의 최소 발굴 비용 / 각 구간에서 먼저 팔 위치 공간 확보하고 0으로 시작
//     for (size_t size = 1; size <= n; ++size) for (size_t left = 0; left + size <= n; ++left) {  // 발굴할 후보 구간 길이 순서대로 확인; 남은 후보의 왼쪽 끝 갱신
//         size_t right = left + size; int best = INT_MAX;  // 남은 후보의 열린 오른쪽 끝 / 이번 구간의 최소 최악 비용 저장
//         for (size_t middle = left; middle < right; ++middle) {  // 먼저 팔 위치 순서대로 확인
//             int first = dp[left * stride + middle], second = dp[(middle + 1) * stride + right]; int cost = depth[middle] + (first > second ? first : second);  // 왼쪽으로 갔을 때 비용 / 오른쪽으로 갔을 때 비용 / 현재 위치 비용과 더 비싼 하위 구간 합 저장
//             if (cost < best) { best = cost; choice[left * stride + right] = (int)middle; }  // 더 싼 굴착 분할점을 찾으면 비용과 실제 선택할 깊이 함께 저장
//         }  // 이 범위 끝
//         dp[left * stride + right] = best;  // 탐색 구간별 최악의 최소 발굴 비용 갱신
//     }  // 이 범위 끝
//     size_t left = 0, right = n; int answer = 0;  // 남은 후보의 왼쪽 끝 / 남은 후보의 열린 오른쪽 끝 / 발견한 보물 위치 저장
//     while (left < right) {  // 굴착 범위가 한 값으로 좁혀질 때까지 선택한 깊이 질의
//         size_t middle = (size_t)choice[left * stride + right]; int result = excavate((int)middle + 1);  // 먼저 팔 위치 / 발굴 콜백의 방향 응답 저장
//         if (!result) { answer = (int)middle + 1; break; }  // 발굴 콜백의 방향 응답가 없으면 발견한 보물 위치 갱신
//         if (result < 0) right = middle; else left = middle + 1;  // 발굴 콜백의 방향 응답가 0보다 작으면 남은 후보의 열린 오른쪽 끝 / 남은 후보의 왼쪽 끝 갱신
//     }  // 이 범위 끝
//     free(dp); free(choice);  // 탐색 구간별 최악의 최소 발굴 비용 / 각 구간에서 먼저 팔 위치 임시 공간 정리
//     return answer;  // 발견한 보물 위치 반환
// }  // 이 범위 끝

// 풀이 요약
// 구간 DP로 현재 굴착 비용 + max(왼쪽 최악 비용, 오른쪽 최악 비용)을 최소화하는 열을 정하기
// excavate의 방향 응답에 따라 그 전략의 왼쪽·오른쪽 구간으로 이동하기; 최소 최악 비용 이하로 항상 찾으므로 보장된 money를 넘지 않음; 시간 O(N³), 공간 O(N²)
// 예: 비용이 모두 1인 5열은 가운데를 먼저 파고, 응답 방향에서 같은 전략을 반복하면 최대 3번 안에 발굴하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:24:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/003_468378_%EB%B3%B4%EB%AC%BC_%EC%B0%BE%EA%B8%B0/README.md)
