# 안전지대

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120866) · Level 0 · C

## 풀이

각 칸을 기준으로 자신과 주변 여덟 칸을 직접 검사. 보드 범위 안에 있는 지뢰가 하나도 없을 때만 안전한 칸으로 셈.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int** board, size_t board_rows, size_t board_cols) {
    int count = 0;
    for (int y = 0; y < (int)board_rows; ++y)
        for (int x = 0; x < (int)board_cols; ++x) {
            bool safe = true;
            for (int dy = -1; dy <= 1; ++dy)
                for (int dx = -1; dx <= 1; ++dx) {
                    int ny = y + dy, nx = x + dx;
                    if (ny >= 0 && ny < (int)board_rows && nx >= 0 && nx < (int)board_cols && board[ny][nx]) safe = false;
                }
            count += safe;
        }
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int** board, size_t board_rows, size_t board_cols) {  // 안전지대 풀이 시작
//     int count = 0;  // 주변에 지뢰가 없는 안전한 칸 수를 0으로 시작
//     for (int y = 0; y < (int)board_rows; ++y)  // 안전 여부를 판단할 모든 행 순회
//         for (int x = 0; x < (int)board_cols; ++x) {  // 현재 행의 각 칸을 안전 여부 판단의 기준점으로 선택
//             bool safe = true;  // 현재 칸 주변에 지뢰가 없다고 가정
//             for (int dy = -1; dy <= 1; ++dy)  // 기준 칸의 위·현재·아래 행 오프셋 선택
//                 for (int dx = -1; dx <= 1; ++dx) {  // 기준 칸의 왼쪽·현재·오른쪽 열 오프셋 선택
//                     int ny = y + dy, nx = x + dx;  // 현재 칸 주변에서 확인할 다음 행·열 좌표
//                     if (ny >= 0 && ny < (int)board_rows && nx >= 0 && nx < (int)board_cols && board[ny][nx]) safe = false;  // 범위 안에 있는 이웃 칸이 지뢰이면 현재 칸도 안전하지 않음
//                 }  // 블록 끝
//             count += safe;  // 현재 칸과 주변 여덟 칸에 지뢰가 없으면 안전한 칸 수에 1 추가
//         }  // 블록 끝
//     return count;  // 전체 보드에서 센 안전한 칸 수 반환
// }  // 블록 끝
// 풀이 요약
// 각 칸을 기준으로 자신과 주변 여덟 칸을 직접 검사. 보드 범위 안에 있는 지뢰가 하나도 없을 때만 안전한 칸으로 셈.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120866_%EC%95%88%EC%A0%84%EC%A7%80%EB%8C%80/README.md)
