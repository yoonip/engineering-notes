# 당구 연습

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/169198) · Level 2 · C

## 풀이

목표 공을 네 벽에 대칭시켜 반사 경로를 직선으로 바꾸기; 벽 전에 목표 공을 먼저 맞히는 방향은 제외하기
예: (3,7)에서 (7,7)은 아래·위 벽 후보 중 위 벽을 거치면 거리 제곱 52.; 공 B개일 때 시간·결과 공간 O(B)

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

int* solution(int m, int n, int startX, int startY, int** balls, size_t balls_rows, size_t balls_cols) {
    (void)balls_cols;
    int* answer = malloc(balls_rows * sizeof(*answer));
    for (size_t i = 0; i < balls_rows; ++i) {
        int x = balls[i][0], y = balls[i][1], best = INT_MAX, dx, dy, distance;
        if (!(startY == y && x < startX)) { dx = startX + x; dy = startY - y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }
        if (!(startY == y && x > startX)) { dx = 2 * m - startX - x; dy = startY - y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }
        if (!(startX == x && y < startY)) { dx = startX - x; dy = startY + y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }
        if (!(startX == x && y > startY)) { dx = startX - x; dy = 2 * n - startY - y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }
        answer[i] = best;
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
// int* solution(int m, int n, int startX, int startY, int** balls, size_t balls_rows, size_t balls_cols) {  // 목표 공을 네 벽에 대칭시켜 반사 경로를 직선으로 바꾸기; 벽 전에 목표 공을 먼저 맞히는 방향은 제외하기
//     (void)balls_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* answer = malloc(balls_rows * sizeof(*answer));  // 공별 한 번 반사 최소 거리 제곱 공간 확보
//     for (size_t i = 0; i < balls_rows; ++i) {  // 목표 공 번호 순서대로 확인
//         int x = balls[i][0], y = balls[i][1], best = INT_MAX, dx, dy, distance;  // 목표 공 x좌표 / 목표 공 y좌표 / 이번 공의 최소 거리 제곱 저장
//         if (!(startY == y && x < startX)) { dx = startX + x; dy = startY - y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }  // 목표 공을 먼저 치는 경우를 빼고 왼쪽 벽에 반사한 거리 제곱 비교
//         if (!(startY == y && x > startX)) { dx = 2 * m - startX - x; dy = startY - y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }  // 목표 공을 먼저 치는 경우를 빼고 오른쪽 벽에 반사한 거리 제곱 비교
//         if (!(startX == x && y < startY)) { dx = startX - x; dy = startY + y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }  // 목표 공을 먼저 치는 경우를 빼고 아래 벽에 반사한 거리 제곱 비교
//         if (!(startX == x && y > startY)) { dx = startX - x; dy = 2 * n - startY - y; distance = dx * dx + dy * dy; if (distance < best) best = distance; }  // 목표 공을 먼저 치는 경우를 빼고 위 벽에 반사한 거리 제곱 비교
//         answer[i] = best;  // 공별 한 번 반사 최소 거리 제곱 갱신
//     }  // 이 범위 끝
//     return answer;  // 공별 한 번 반사 최소 거리 제곱 반환
// }  // 이 범위 끝

// 풀이 요약
// 목표 공을 네 벽에 대칭시켜 반사 경로를 직선으로 바꾸기; 벽 전에 목표 공을 먼저 맞히는 방향은 제외하기
// 예: (3,7)에서 (7,7)은 아래·위 벽 후보 중 위 벽을 거치면 거리 제곱 52.; 공 B개일 때 시간·결과 공간 O(B)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:11:24
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/020_169198_%EB%8B%B9%EA%B5%AC_%EC%97%B0%EC%8A%B5/README.md)
