# 안티세포

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86054) · Level 4 · C

## 풀이

같은 질량끼리 합성하므로 마지막 원소의 질량은 두 배씩만 커짐; 각 끝점에 가능한 최대 합성 횟수만 저장

양수 배열이라 같은 합의 구간 경계는 유일하기; 한 세포의 합성 순서도 유일하므로, 마지막 세포의 시작별로 앞부분 DP를 합산하기

예: [1,1,1,1]은 기록 6가지; 전체 원소 수 N, 전체 질량 S일 때 시간 O(N*log S), 공간 O(N)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static size_t locate(const long long* prefix, size_t high, long long target) { size_t low = 0; while (low < high) { size_t mid = (low + high) / 2; if (prefix[mid] < target) low = mid + 1; else high = mid; } return low; }
int* solution(int a[], size_t a_len, int s[], size_t s_len) {
    (void)a_len; const int mod = 1000000007; int* answer = malloc(s_len * sizeof(*answer)); size_t offset = 0;
    for (size_t group = 0; group < s_len; ++group) {
        size_t length = (size_t)s[group]; long long* prefix = calloc(length + 1,sizeof(*prefix)); int* depth = calloc(length,sizeof(*depth)); int* dp = malloc((length + 1) * sizeof(*dp)); dp[0] = 1;
        for (size_t right = 0; right < length; ++right) {
            long long value = a[offset + right]; prefix[right + 1] = prefix[right] + value; size_t left = right; long long mass = value, ways = dp[right];
            while (left > 0) {
                size_t previous = left - 1; long long divisor = a[offset + previous], ratio = mass / divisor;
                if (mass % divisor || ratio == 0 || (ratio & (ratio - 1))) break;
                int required = 0; for (long long r = ratio; r > 1; r >>= 1) ++required;
                if (required > depth[previous]) break;
                left = locate(prefix,left + 1,prefix[left] - mass); mass *= 2; ++depth[right]; ways = (ways + dp[left]) % mod;
            }
            dp[right + 1] = (int)ways;
        }
        answer[group] = dp[length]; offset += length; free(prefix); free(depth); free(dp);
    }
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
// static size_t locate(const long long* prefix, size_t high, long long target) { size_t low = 0; while (low < high) { size_t mid = (low + high) / 2; if (prefix[mid] < target) low = mid + 1; else high = mid; } return low; }  // 목표 누적합이 있는 위치를 이분 탐색
// int* solution(int a[], size_t a_len, int s[], size_t s_len) {  // 같은 질량끼리 합성하므로 마지막 원소의 질량은 두 배씩만 커짐; 각 끝점에 가능한 최대 합성 횟수만 저장
//     (void)a_len; const int mod = 1000000007; int* answer = malloc(s_len * sizeof(*answer)); size_t offset = 0;  // 질의 묶음별 합칠 수 있는 경우의 수 / 원래 배열에서 이번 묶음 시작 공간 확보
//     for (size_t group = 0; group < s_len; ++group) {  // 현재 묶음 번호 순서대로 확인
//         size_t length = (size_t)s[group]; long long* prefix = calloc(length + 1,sizeof(*prefix)); int* depth = calloc(length,sizeof(*depth)); int* dp = malloc((length + 1) * sizeof(*dp)); dp[0] = 1;  // 이번 묶음 길이 / 현재 묶음의 질량 누적합 / 오른쪽 끝별 합칠 수 있는 깊이 / 접두사별 합치기 경우의 수 공간 확보하고 0으로 시작
//         for (size_t right = 0; right < length; ++right) {  // 이번에 추가한 세포 위치 순서대로 확인
//             long long value = a[offset + right]; prefix[right + 1] = prefix[right] + value; size_t left = right; long long mass = value, ways = dp[right];  // 현재 세포까지 누적 질량을 늘리고 이 위치부터 가능한 마지막 덩어리 계산
//             while (left > 0) {  // 현재 합쳐진 덩어리의 왼쪽가 0보다 크면 반복
//                 size_t previous = left - 1; long long divisor = a[offset + previous], ratio = mass / divisor;  // 왼쪽 원래 세포의 질량과 현재 덩어리의 질량 비율 계산
//                 if (mass % divisor || ratio == 0 || (ratio & (ratio - 1))) break;  // 질량 비가 정수인 2의 거듭제곱이 아니면 더 합칠 수 없음
//                 int required = 0; for (long long r = ratio; r > 1; r >>= 1) ++required;  // 그 비율에 필요한 이진 병합 깊이 / 질량 비율을 줄일 사본 저장
//                 if (required > depth[previous]) break;  // 왼쪽 덩어리가 필요한 이진 병합 깊이까지 커질 수 없으면 중단
//                 left = locate(prefix,left + 1,prefix[left] - mass); mass *= 2; ++depth[right]; ways = (ways + dp[left]) % mod;  // 현재 합쳐진 덩어리의 왼쪽 / 현재 오른쪽 끝까지 가능한 경우의 수 갱신
//             }  // 이 범위 끝
//             dp[right + 1] = (int)ways;  // 접두사별 합치기 경우의 수 갱신
//         }  // 이 범위 끝
//         answer[group] = dp[length]; offset += length; free(prefix); free(depth); free(dp);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     }  // 이 범위 끝
//     return answer;  // 질의 묶음별 합칠 수 있는 경우의 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 같은 질량끼리 합성하므로 마지막 원소의 질량은 두 배씩만 커짐; 각 끝점에 가능한 최대 합성 횟수만 저장
// 양수 배열이라 같은 합의 구간 경계는 유일하기; 한 세포의 합성 순서도 유일하므로, 마지막 세포의 시작별로 앞부분 DP를 합산하기
// 예: [1,1,1,1]은 기록 6가지; 전체 원소 수 N, 전체 질량 S일 때 시간 O(N*log S), 공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:37:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level4/extra_86054_%EC%95%88%ED%8B%B0%EC%84%B8%ED%8F%AC/README.md)
