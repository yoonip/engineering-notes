# 공원 산책

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/172928) · Level 1 · C

## 풀이

시작 칸을 찾고 명령의 이동 경로를 한 칸씩 확인; 공원 밖이나 장애물을 만나는 명령은 적용하지 않음

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int* solution(const char* park[], size_t park_len, const char* routes[], size_t routes_len) {
    int height = (int)park_len, width = (int)strlen(park[0]), row = 0, col = 0;
    for (int r = 0; r < height; ++r) for (int c = 0; c < width; ++c) if (park[r][c] == 'S') { row = r; col = c; }
    for (size_t q = 0; q < routes_len; ++q) {
        char direction; int distance; sscanf(routes[q], "%c %d", &direction, &distance);
        int dr = direction == 'N' ? -1 : direction == 'S' ? 1 : 0;
        int dc = direction == 'W' ? -1 : direction == 'E' ? 1 : 0;
        int nr = row, nc = col; bool valid = true;
        for (int step = 0; step < distance; ++step) {
            nr += dr; nc += dc;
            if (nr < 0 || nr >= height || nc < 0 || nc >= width || park[nr][nc] == 'X') { valid = false; break; }
        }
        if (valid) { row = nr; col = nc; }
    }
    int* answer = malloc(2 * sizeof(int)); answer[0] = row; answer[1] = col;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int* solution(const char* park[], size_t park_len, const char* routes[], size_t routes_len) {  // 시작 칸을 찾고 명령의 이동 경로를 한 칸씩 확인; 공원 밖이나 장애물을 만나는 명령은 적용하지 않음
//     int height = (int)park_len, width = (int)strlen(park[0]), row = 0, col = 0;  // 공원의 행 수 / 공원의 열 수 / 현재 행 / 현재 열 저장
//     for (int r = 0; r < height; ++r) for (int c = 0; c < width; ++c) if (park[r][c] == 'S') { row = r; col = c; }  // 출발점을 찾을 행 순서대로 확인; 출발점을 찾을 열 갱신
//     for (size_t q = 0; q < routes_len; ++q) {  // 현재 이동 명령 순서대로 확인
//         char direction; int distance; sscanf(routes[q], "%c %d", &direction, &distance);  // 이동 방향 문자와 이동할 칸 수 읽기
//         int dr = direction == 'N' ? -1 : direction == 'S' ? 1 : 0;  // 한 걸음의 행 변화 저장
//         int dc = direction == 'W' ? -1 : direction == 'E' ? 1 : 0;  // 한 걸음의 열 변화 저장
//         int nr = row, nc = col; bool valid = true;  // 이동을 시험할 행 / 이동을 시험할 열 / 명령 전체를 끝낼 수 있는지 여부 저장
//         for (int step = 0; step < distance; ++step) {  // 시험 중인 걸음 번호 순서대로 확인
//             nr += dr; nc += dc;  // 이동을 시험할 행 / 한 걸음의 행 변화 / 이동을 시험할 열 더해 누적
//             if (nr < 0 || nr >= height || nc < 0 || nc >= width || park[nr][nc] == 'X') { valid = false; break; }  // 격자 밖이거나 막혔거나 이미 처리한 칸이면 명령 전체를 끝낼 수 있는지 여부 갱신
//         }  // 이 범위 끝
//         if (valid) { row = nr; col = nc; }  // 명령 전체를 끝낼 수 있는지 여부가 남아 있으면 현재 행 / 현재 열 갱신
//     }  // 이 범위 끝
//     int* answer = malloc(2 * sizeof(int)); answer[0] = row; answer[1] = col;  // 명령 처리 후 최종 좌표 공간 확보
//     return answer;  // 명령 처리 후 최종 좌표 반환
// }  // 이 범위 끝

// 풀이 요약
// 시작 칸을 찾고 명령의 이동 경로를 한 칸씩 확인; 공원 밖이나 장애물을 만나는 명령은 적용하지 않음
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:46:13
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_172928_%EA%B3%B5%EC%9B%90_%EC%82%B0%EC%B1%85/README.md)
