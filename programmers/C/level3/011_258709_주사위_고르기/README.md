# 주사위 고르기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258709) · Level 3 · C

## 풀이

A가 고를 절반의 주사위 조합을 모두 비교; 선택마다 A·B의 합별 경우의 수를 구하고 B의 누적 빈도로 A가 이기는 횟수 합산
무승부는 이긴 경우에 넣지 않음; 각 선택의 전체 경우 수가 같으므로 승리 횟수가 가장 큰 조합이 답; N≤10, 합 범위≤500을 이용하기
예: 첫 예제에서 1·4번 주사위는 616가지 승리로 최댓값이므로 [1,4]를 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static void distribution(int** dice, int n, unsigned mask, int* result) {
    int temp[501]; memset(result, 0, 501 * sizeof(*result)); result[0] = 1; int maximum = 0;
    for (int i = 0; i < n; ++i) if (mask & (1u << i)) {
        memset(temp, 0, sizeof(temp));
        for (int sum = 0; sum <= maximum; ++sum) if (result[sum]) for (int face = 0; face < 6; ++face) temp[sum + dice[i][face]] += result[sum];
        maximum += 100; memcpy(result, temp, sizeof(temp));
    }
}
int* solution(int** dice, size_t dice_rows, size_t dice_cols) {
    (void)dice_cols; int n = (int)dice_rows, half = n / 2; unsigned full = (1u << n) - 1;
    int* answer = malloc((size_t)half * sizeof(*answer)); long long best = -1;
    for (unsigned mask = 0; mask <= full; ++mask) if (__builtin_popcount(mask) == half) {
        int left[501], right[501]; distribution(dice, n, mask, left); distribution(dice, n, full ^ mask, right);
        long long wins = 0, cumulative = 0;
        for (int sum = 0; sum <= 500; ++sum) { wins += (long long)left[sum] * cumulative; cumulative += right[sum]; }
        bool better = wins > best;
        if (wins == best) { int pos = 0; for (int i = 0; i < n; ++i) if (mask & (1u << i)) { if (i + 1 != answer[pos]) { better = i + 1 < answer[pos]; break; } ++pos; } }
        if (better) { best = wins; int pos = 0; for (int i = 0; i < n; ++i) if (mask & (1u << i)) answer[pos++] = i + 1; }
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
// static void distribution(int** dice, int n, unsigned mask, int* result) {  // 선택한 주사위의 합별 경우의 수 계산
//     int temp[501]; memset(result, 0, 501 * sizeof(*result)); result[0] = 1; int maximum = 0;  // 주사위 합별 경우의 수 / 지금까지 가능한 합의 상한 초기화
//     for (int i = 0; i < n; ++i) if (mask & (1u << i)) {  // 선택한 비트에 해당하는 주사위만 합 분포에 반영
//         memset(temp, 0, sizeof(temp));  // 주사위 하나를 더한 분포 초기화
//         for (int sum = 0; sum <= maximum; ++sum) if (result[sum]) for (int face = 0; face < 6; ++face) temp[sum + dice[i][face]] += result[sum];  // 가능한 기존 합마다 새 주사위의 여섯 면을 더해 합별 경우의 수 누적
//         maximum += 100; memcpy(result, temp, sizeof(temp));  // 지금까지 가능한 합의 상한 / 주사위 합별 경우의 수 / 주사위 하나를 더한 분포 복사
//     }  // 이 범위 끝
// }  // 이 범위 끝
// int* solution(int** dice, size_t dice_rows, size_t dice_cols) {  // A가 고를 절반의 주사위 조합을 모두 비교; 선택마다 A·B의 합별 경우의 수를 구하고 B의 누적 빈도로 A가 이기는 횟수 합산
//     (void)dice_cols; int n = (int)dice_rows, half = n / 2; unsigned full = (1u << n) - 1;  // 주사위 수 / 뽑을 주사위 수 / 전체 주사위 비트 비트 상태 갱신
//     int* answer = malloc((size_t)half * sizeof(*answer)); long long best = -1;  // 승리 확률이 가장 높은 주사위 번호 / 가장 많이 이긴 경우의 수 공간 확보
//     for (unsigned mask = 0; mask <= full; ++mask) if (__builtin_popcount(mask) == half) {  // 전체 주사위 중 정확히 절반을 고른 부분집합만 비교
//         int left[501], right[501]; distribution(dice, n, mask, left); distribution(dice, n, full ^ mask, right);  // 내 주사위 합의 분포 / 상대 주사위 합의 분포 / 주사위 수 / 선택한 주사위 비트 확인
//         long long wins = 0, cumulative = 0;  // 이 선택으로 이기는 경우의 수 / 현재 합보다 작은 상대 경우의 수 저장
//         for (int sum = 0; sum <= 500; ++sum) { wins += (long long)left[sum] * cumulative; cumulative += right[sum]; }  // 분포의 합 위치 순서대로 확인; 이 선택으로 이기는 경우의 수 / 내 주사위 합의 분포 / 분포의 합 위치 더해 누적
//         bool better = wins > best;  // 동률 우선순서까지 더 좋은 선택인지 여부 저장
//         if (wins == best) { int pos = 0; for (int i = 0; i < n; ++i) if (mask & (1u << i)) { if (i + 1 != answer[pos]) { better = i + 1 < answer[pos]; break; } ++pos; } }  // 승리 횟수가 같으면 선택한 주사위 번호 목록의 사전순으로 결정
//         if (better) { best = wins; int pos = 0; for (int i = 0; i < n; ++i) if (mask & (1u << i)) answer[pos++] = i + 1; }  // 동률 우선순서까지 더 좋은 선택인지 여부가 남아 있으면 가장 많이 이긴 경우의 수 / 고른 주사위 번호를 쓸 위치 / 주사위 위치 / 승리 확률이 가장 높은 주사위 번호 갱신
//     }  // 이 범위 끝
//     return answer;  // 승리 확률이 가장 높은 주사위 번호 반환
// }  // 이 범위 끝

// 풀이 요약
// A가 고를 절반의 주사위 조합을 모두 비교; 선택마다 A·B의 합별 경우의 수를 구하고 B의 누적 빈도로 A가 이기는 횟수 합산
// 무승부는 이긴 경우에 넣지 않음; 각 선택의 전체 경우 수가 같으므로 승리 횟수가 가장 큰 조합이 답; N≤10, 합 범위≤500을 이용하기
// 예: 첫 예제에서 1·4번 주사위는 616가지 승리로 최댓값이므로 [1,4]를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/011_258709_%EC%A3%BC%EC%82%AC%EC%9C%84_%EA%B3%A0%EB%A5%B4%EA%B8%B0/README.md)
