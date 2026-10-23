# 격자 뒤집기 미로

[레벨 4 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389630) · Level 4 · C

## 풀이

양쪽 길이가 짝수면 홀수 색 칸 하나만 빼고, 그 외에는 모든 칸을 방문하는 경로가 있음; 양수 점수라 더 뺄 필요가 없음
행 뒤집기 2^n가지를 고정하면 각 열은 독립적으로 선택됨; 짝수×짝수에서는 한 칸 제외 손실도 함께 비교
예: [[1,2],[3,4]], 숨은 면 [[5,6],[7,8]], k=0이면 5+7+8=20.; 시간 O(2^n*n*m), 추가 공간 O(n)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int** visible, size_t visible_rows, size_t visible_cols, int** hidden, size_t hidden_rows, size_t hidden_cols, int k) {
    (void)hidden_rows; (void)hidden_cols; int n = (int)visible_rows, m = (int)visible_cols, answer = INT_MIN; bool skip = n % 2 == 0 && m % 2 == 0;
    for (unsigned mask = 0; mask < (1u << n); ++mask) {
        int total = -k * __builtin_popcount(mask), best_loss = INT_MIN;
        for (int c = 0; c < m; ++c) {
            int front = 0, back = 0, low_front = 101, low_back = 101;
            for (int r = 0; r < n; ++r) {
                int a = visible[r][c], b = hidden[r][c]; if (mask & (1u << r)) { int temp = a; a = b; b = temp; }
                front += a; back += b;
                if (skip && (r + c) % 2) { if (a < low_front) low_front = a; if (b < low_back) low_back = b; }
            }
            int normal = front > back - k ? front : back - k; total += normal;
            if (skip) { int reduced = front - low_front > back - low_back - k ? front - low_front : back - low_back - k; if (reduced - normal > best_loss) best_loss = reduced - normal; }
        }
        if (skip) total += best_loss; if (total > answer) answer = total;
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
// int solution(int** visible, size_t visible_rows, size_t visible_cols, int** hidden, size_t hidden_rows, size_t hidden_cols, int k) {  // 양쪽 길이가 짝수면 홀수 색 칸 하나만 빼고, 그 외에는 모든 칸을 방문하는 경로가 있음; 양수 점수라 더 뺄 필요가 없음
//     (void)hidden_rows; (void)hidden_cols; int n = (int)visible_rows, m = (int)visible_cols, answer = INT_MIN; bool skip = n % 2 == 0 && m % 2 == 0;  // 격자 행 수 / 격자 열 수 / 이동 조건과 뒤집기 비용을 적용한 최대 합 / 짝수 곱하기 짝수 격자라 한 칸을 빼야 하는지 여부 갱신
//     for (unsigned mask = 0; mask < (1u << n); ++mask) {  // 남은 후보를 순서대로 확인
//         int total = -k * __builtin_popcount(mask), best_loss = INT_MIN;  // 행 뒤집기 비용을 반영한 합 / 한 칸 제외 시 손실이 가장 적은 선택 저장
//         for (int c = 0; c < m; ++c) {  // 선택할 열 순서대로 확인
//             int front = 0, back = 0, low_front = 101, low_back = 101;  // 현재 열의 앞면 합 / 현재 열의 뒷면 합 / 제외 가능한 앞면 값의 최솟값 / 제외 가능한 뒷면 값의 최솟값 저장
//             for (int r = 0; r < n; ++r) {  // 열 안의 행 순서대로 확인
//                 int a = visible[r][c], b = hidden[r][c]; if (mask & (1u << r)) { int temp = a; a = b; b = temp; }  // 행 뒤집기를 적용한 앞면 값 / 행 뒤집기를 적용한 뒷면 값 저장
//                 front += a; back += b;  // 현재 열의 앞면 합 / 행 뒤집기를 적용한 앞면 값 / 현재 열의 뒷면 합 더해 누적
//                 if (skip && (r + c) % 2) { if (a < low_front) low_front = a; if (b < low_back) low_back = b; }  // 한 칸을 빼야 하는 홀수 색 칸에서 앞면·뒷면의 최소 손실 후보 기록
//             }  // 이 범위 끝
//             int normal = front > back - k ? front : back - k; total += normal;  // 열을 뒤집거나 유지할 때의 최선 합 저장
//             if (skip) { int reduced = front - low_front > back - low_back - k ? front - low_front : back - low_back - k; if (reduced - normal > best_loss) best_loss = reduced - normal; }  // 짝수 곱하기 짝수 격자라 한 칸을 빼야 하는지 여부가 남아 있으면 한 칸을 뺀 뒤 현재 열의 최선 합 / 한 칸 제외 시 손실이 가장 적은 선택 저장
//         }  // 이 범위 끝
//         if (skip) total += best_loss; if (total > answer) answer = total;  // 짝수 곱하기 짝수 격자라 한 칸을 빼야 하는지 여부가 남아 있으면 행 뒤집기 비용을 반영한 합 / 한 칸 제외 시 손실이 가장 적은 선택 / 이동 조건과 뒤집기 비용을 적용한 최대 합 더해 누적
//     }  // 이 범위 끝
//     return answer;  // 이동 조건과 뒤집기 비용을 적용한 최대 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 양쪽 길이가 짝수면 홀수 색 칸 하나만 빼고, 그 외에는 모든 칸을 방문하는 경로가 있음; 양수 점수라 더 뺄 필요가 없음
// 행 뒤집기 2^n가지를 고정하면 각 열은 독립적으로 선택됨; 짝수×짝수에서는 한 칸 제외 손실도 함께 비교
// 예: [[1,2],[3,4]], 숨은 면 [[5,6],[7,8]], k=0이면 5+7+8=20.; 시간 O(2^n*n*m), 추가 공간 O(n)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:35:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level4/extra_389630_%EA%B2%A9%EC%9E%90_%EB%92%A4%EC%A7%91%EA%B8%B0_%EB%AF%B8%EB%A1%9C/README.md)
