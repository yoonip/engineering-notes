# 고고학 최고의 발견

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131702) · Level 3 · C

## 풀이

첫 행의 회전 횟수를 각각 0~3으로 정하면, 위 행을 0으로 맞추기 위한 아래 행의 회전 횟수는 하나로 결정됩니다.
현재 방향에 위·자신·좌우 회전의 영향을 더한 뒤, 합을 4의 배수로 만드는 아래쪽 회전을 계산합니다. 마지막 행에서는 아래쪽 회전이 필요 없어야 합니다. 한 변이 N이면 시간은 O(4^N N²), 회전 상태 공간은 O(N)입니다.
예를 들어 위 칸의 방향이 3이면 바로 아래 시계를 한 번 돌려 위 칸을 0으로 만듭니다. 아래 행들은 차례대로 결정되므로 첫 행의 선택만 모두 탐색합니다.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int** clockHands, size_t clockHands_rows, size_t clockHands_cols) {
    (void)clockHands_cols; int n = (int)clockHands_rows, answer = 3 * n * n + 1; unsigned limit = 1u << (2 * n);
    for (unsigned mask = 0; mask < limit; ++mask) {
        int previous[8] = {0}, current[8] = {0}, needed[8], cost = 0;
        for (int c = 0; c < n; ++c) { current[c] = (mask >> (2 * c)) & 3u; cost += current[c]; }
        for (int r = 0; r < n && cost < answer; ++r) {
            int next_cost = 0;
            for (int c = 0; c < n; ++c) {
                int sum = clockHands[r][c] + previous[c] + current[c] + (c ? current[c - 1] : 0) + (c + 1 < n ? current[c + 1] : 0);
                needed[c] = (4 - sum % 4) % 4; next_cost += needed[c];
            }
            if (r == n - 1) { if (!next_cost) answer = cost; break; }
            cost += next_cost; memcpy(previous, current, (size_t)n * sizeof(*current)); memcpy(current, needed, (size_t)n * sizeof(*needed));
        }
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
// int solution(int** clockHands, size_t clockHands_rows, size_t clockHands_cols) {  // 첫 행의 회전 횟수를 각각 0~3으로 정하면, 위 행을 0으로 맞추기 위한 아래 행의 회전 횟수는 하나로 결정됩니다.
//     (void)clockHands_cols; int n = (int)clockHands_rows, answer = 3 * n * n + 1; unsigned limit = 1u << (2 * n);  // 시계 격자 한 변 / 찾은 최소 회전 수 / 첫 행 회전 조합 수 비트 상태 갱신
//     for (unsigned mask = 0; mask < limit; ++mask) {  // 남은 후보를 순서대로 확인
//         int previous[8] = {0}, current[8] = {0}, needed[8], cost = 0;  // 직전 행에 준 회전 수 / 현재 행의 회전 수 / 지금까지 회전한 횟수 저장
//         for (int c = 0; c < n; ++c) { current[c] = (mask >> (2 * c)) & 3u; cost += current[c]; }  // 시계 열 순서대로 확인; 현재 행의 회전 수 갱신
//         for (int r = 0; r < n && cost < answer; ++r) {  // 처리할 시계 행 순서대로 확인
//             int next_cost = 0;  // 다음 행에 필요한 회전 합 저장
//             for (int c = 0; c < n; ++c) {  // 시계 열 순서대로 확인
//                 int sum = clockHands[r][c] + previous[c] + current[c] + (c ? current[c - 1] : 0) + (c + 1 < n ? current[c + 1] : 0);  // 이웃 회전까지 반영한 시계 방향 저장
//                 needed[c] = (4 - sum % 4) % 4; next_cost += needed[c];  // 아래 행에 강제할 회전 수 갱신
//             }  // 이 범위 끝
//             if (r == n - 1) { if (!next_cost) answer = cost; break; }  // 마지막 행 아래에는 시계가 없으므로 추가 회전이 필요하지 않을 때만 답 갱신
//             cost += next_cost; memcpy(previous, current, (size_t)n * sizeof(*current)); memcpy(current, needed, (size_t)n * sizeof(*needed));  // 지금까지 회전한 횟수 / 다음 행에 필요한 회전 합 / 직전 행에 준 회전 수 복사
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     return answer;  // 찾은 최소 회전 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 첫 행의 회전 횟수를 각각 0~3으로 정하면, 위 행을 0으로 맞추기 위한 아래 행의 회전 횟수는 하나로 결정됩니다.
// 현재 방향에 위·자신·좌우 회전의 영향을 더한 뒤, 합을 4의 배수로 만드는 아래쪽 회전을 계산합니다. 마지막 행에서는 아래쪽 회전이 필요 없어야 합니다. 한 변이 N이면 시간은 O(4^N N²), 회전 상태 공간은 O(N)입니다.
// 예를 들어 위 칸의 방향이 3이면 바로 아래 시계를 한 번 돌려 위 칸을 0으로 만듭니다. 아래 행들은 차례대로 결정되므로 첫 행의 선택만 모두 탐색합니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/028_131702_%EA%B3%A0%EA%B3%A0%ED%95%99_%EC%B5%9C%EA%B3%A0%EC%9D%98_%EB%B0%9C%EA%B2%AC/README.md)
