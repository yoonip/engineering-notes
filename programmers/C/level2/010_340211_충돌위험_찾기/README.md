# [PCCP 기출문제] 3번 / 충돌위험 찾기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340211) · Level 2 · C

## 풀이

매 초 로봇의 현재 좌표를 세고, 행 우선으로 한 칸 움직여 다음 초 상태를 만들기
0초와 마지막 도착 순간을 포함하며, 센터를 떠난 로봇은 다음 초부터 제외하기; 시간 O(로봇 수*최대 이동 시간), 공간 O(로봇 수)
예: 같은 초 (4,4)에 네 대가 모여도 위험 상황은 1번; 서로 다른 두 좌표에서 모이면 2번

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

int solution(int** points, size_t points_rows, size_t points_cols, int** routes, size_t routes_rows, size_t routes_cols) {
    (void)points_cols;
    int max_r = 0, max_c = 0;
    for (size_t i = 0; i < points_rows; ++i) { if (points[i][0] > max_r) max_r = points[i][0]; if (points[i][1] > max_c) max_c = points[i][1]; }
    int* row = malloc(routes_rows * sizeof(*row)); int* col = malloc(routes_rows * sizeof(*col));
    size_t* index = malloc(routes_rows * sizeof(*index)); bool* active = malloc(routes_rows * sizeof(*active));
    int* counts = calloc((size_t)(max_r + 1) * (max_c + 1), sizeof(*counts));
    for (size_t i = 0; i < routes_rows; ++i) { row[i] = points[routes[i][0] - 1][0]; col[i] = points[routes[i][0] - 1][1]; index[i] = 1; active[i] = true; }
    size_t remaining = routes_rows; int answer = 0;
    while (remaining) {
        memset(counts, 0, (size_t)(max_r + 1) * (max_c + 1) * sizeof(*counts));
        for (size_t i = 0; i < routes_rows; ++i) if (active[i]) {
            int at = row[i] * (max_c + 1) + col[i]; if (++counts[at] == 2) ++answer;
            if (index[i] == routes_cols) { active[i] = false; --remaining; continue; }
            int target = routes[i][index[i]] - 1, target_r = points[target][0], target_c = points[target][1];
            if (row[i] != target_r) row[i] += row[i] < target_r ? 1 : -1;
            else if (col[i] != target_c) col[i] += col[i] < target_c ? 1 : -1;
            if (row[i] == target_r && col[i] == target_c) ++index[i];
        }
    }
    free(row); free(col); free(index); free(active); free(counts);
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
// int solution(int** points, size_t points_rows, size_t points_cols, int** routes, size_t routes_rows, size_t routes_cols) {  // 매 초 로봇의 현재 좌표를 세고, 행 우선으로 한 칸 움직여 다음 초 상태를 만들기
//     (void)points_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int max_r = 0, max_c = 0;  // 점들의 최대 행 / 점들의 최대 열 저장
//     for (size_t i = 0; i < points_rows; ++i) { if (points[i][0] > max_r) max_r = points[i][0]; if (points[i][1] > max_c) max_c = points[i][1]; }  // 로봇 또는 지점 번호 순서대로 확인; 점들의 최대 행 / 점들의 최대 열 갱신
//     int* row = malloc(routes_rows * sizeof(*row)); int* col = malloc(routes_rows * sizeof(*col));  // 로봇별 현재 행 / 로봇별 현재 열 공간 확보
//     size_t* index = malloc(routes_rows * sizeof(*index)); bool* active = malloc(routes_rows * sizeof(*active));  // 로봇별 다음 목표 번호 / 아직 운행 중인 로봇 표시 공간 확보
//     int* counts = calloc((size_t)(max_r + 1) * (max_c + 1), sizeof(*counts));  // 이번 초의 칸별 로봇 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < routes_rows; ++i) { row[i] = points[routes[i][0] - 1][0]; col[i] = points[routes[i][0] - 1][1]; index[i] = 1; active[i] = true; }  // 로봇 또는 지점 번호 순서대로 확인; 로봇별 현재 행 / 로봇별 현재 열 / 로봇별 다음 목표 번호 / 아직 운행 중인 로봇 표시 갱신
//     size_t remaining = routes_rows; int answer = 0;  // 운행 중인 로봇 수 / 동시에 두 대 이상 모인 위험 횟수 저장
//     while (remaining) {  // 운행 중인 로봇 수가 남아 있으면 반복
//         memset(counts, 0, (size_t)(max_r + 1) * (max_c + 1) * sizeof(*counts));  // 이번 초의 칸별 로봇 수 / 점들의 최대 행 / 점들의 최대 열 초기화
//         for (size_t i = 0; i < routes_rows; ++i) if (active[i]) {  // 아직 최종 지점까지 운행 중인 로봇만 한 초 이동
//             int at = row[i] * (max_c + 1) + col[i]; if (++counts[at] == 2) ++answer;  // 현재 칸 일차원 위치 저장
//             if (index[i] == routes_cols) { active[i] = false; --remaining; continue; }  // 경로의 모든 지점에 도착했으면 운행 종료 표시하고 남은 로봇 수 줄이기
//             int target = routes[i][index[i]] - 1, target_r = points[target][0], target_c = points[target][1];  // 다음 목표 지점 번호 / 목표 행 / 목표 열 저장
//             if (row[i] != target_r) row[i] += row[i] < target_r ? 1 : -1;  // 목표 행에 아직 못 왔으면 행부터 한 칸 이동
//             else if (col[i] != target_c) col[i] += col[i] < target_c ? 1 : -1;  // 목표 행에 도착한 뒤에는 목표 열 쪽으로 한 칸 이동
//             if (row[i] == target_r && col[i] == target_c) ++index[i];  // 목표 행과 열에 모두 도착했으면 다음 경로 지점으로 넘기기
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(row); free(col); free(index); free(active); free(counts);  // 로봇별 현재 행 / 로봇별 현재 열 / 로봇별 다음 목표 번호 / 아직 운행 중인 로봇 표시 임시 공간 정리
//     return answer;  // 동시에 두 대 이상 모인 위험 횟수 반환
// }  // 이 범위 끝

// 풀이 요약
// 매 초 로봇의 현재 좌표를 세고, 행 우선으로 한 칸 움직여 다음 초 상태를 만들기
// 0초와 마지막 도착 순간을 포함하며, 센터를 떠난 로봇은 다음 초부터 제외하기; 시간 O(로봇 수*최대 이동 시간), 공간 O(로봇 수)
// 예: 같은 초 (4,4)에 네 대가 모여도 위험 상황은 1번; 서로 다른 두 좌표에서 모이면 2번
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:08:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/010_340211_%EC%B6%A9%EB%8F%8C%EC%9C%84%ED%97%98_%EC%B0%BE%EA%B8%B0/README.md)
