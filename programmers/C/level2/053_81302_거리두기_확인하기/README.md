# 거리두기 확인하기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/81302) · Level 2 · C

## 풀이

모든 사람 쌍 중 거리 1은 위반, 거리 2는 사이의 경로가 파티션으로 막혔는지 확인
예: 예제의 둘째 방만 위반해 [1,0,1,1,1].; 한 방의 사람 수 P일 때 시간 O(P²), 공간 O(P); 방 크기는 5×5 고정

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

static int valid(const char** room) {
    for (int r = 0; r < 5; ++r) for (int c = 0; c < 5; ++c) {
        if (room[r][c] != 'P') continue;
        for (int nr = r; nr < 5; ++nr) for (int nc = 0; nc < 5; ++nc) {
            if (nr == r && nc <= c) continue;
            if (room[nr][nc] != 'P') continue;
            int distance = abs(r - nr) + abs(c - nc);
            if (distance == 1) return 0;
            if (distance == 2) {
                if (r == nr && room[r][(c + nc) / 2] != 'X') return 0;
                if (c == nc && room[(r + nr) / 2][c] != 'X') return 0;
                if (r != nr && c != nc && (room[r][nc] != 'X' || room[nr][c] != 'X')) return 0;
            }
        }
    }
    return 1;
}
int* solution(const char*** places, size_t places_rows, size_t places_cols) {
    (void)places_cols;
    int* answer = malloc(places_rows * sizeof(*answer));
    for (size_t i = 0; i < places_rows; ++i) answer[i] = valid(places[i]);
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
// static int valid(const char** room) {  // 조건을 모두 지키는 구조인지 확인
//     for (int r = 0; r < 5; ++r) for (int c = 0; c < 5; ++c) {  // 첫 사람 행 순서대로 확인; 첫 사람 열 갱신
//         if (room[r][c] != 'P') continue;  // 사람 P가 아닌 칸은 첫 사람 후보에서 제외
//         for (int nr = r; nr < 5; ++nr) for (int nc = 0; nc < 5; ++nc) {  // 둘째 사람 행 순서대로 확인; 둘째 사람 열 갱신
//             if (nr == r && nc <= c) continue;  // 같은 줄에서 앞서 검사한 사람 쌍은 중복 확인하지 않기
//             if (room[nr][nc] != 'P') continue;  // 둘째 위치도 사람 P인 경우만 거리두기 검사
//             int distance = abs(r - nr) + abs(c - nc);  // 두 사람의 맨해튼 거리 저장
//             if (distance == 1) return 0;  // 두 사람의 맨해튼 거리가 1이면 더 이어갈 수 없으면 0
//             if (distance == 2) {  // 두 사람의 맨해튼 거리가 2이면 처리
//                 if (r == nr && room[r][(c + nc) / 2] != 'X') return 0;  // 가로로 두 칸 떨어졌는데 중간이 파티션이 아니면 거리두기 위반
//                 if (c == nc && room[(r + nr) / 2][c] != 'X') return 0;  // 세로로 두 칸 떨어졌는데 중간이 파티션이 아니면 거리두기 위반
//                 if (r != nr && c != nc && (room[r][nc] != 'X' || room[nr][c] != 'X')) return 0;  // 대각선 두 사람 사이의 두 경유 칸 중 하나라도 열려 있으면 위반
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     return 1;  // 검사한 모든 사람 쌍이 거리두기를 지켰으면 1
// }  // 이 범위 끝
// int* solution(const char*** places, size_t places_rows, size_t places_cols) {  // 모든 사람 쌍 중 거리 1은 위반, 거리 2는 사이의 경로가 파티션으로 막혔는지 확인
//     (void)places_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* answer = malloc(places_rows * sizeof(*answer));  // 대기실별 거리두기 여부 공간 확보
//     for (size_t i = 0; i < places_rows; ++i) answer[i] = valid(places[i]);  // 검사할 대기실 번호 순서대로 확인; 대기실별 거리두기 여부 갱신
//     return answer;  // 대기실별 거리두기 여부 반환
// }  // 이 범위 끝

// 풀이 요약
// 모든 사람 쌍 중 거리 1은 위반, 거리 2는 사이의 경로가 파티션으로 막혔는지 확인
// 예: 예제의 둘째 방만 위반해 [1,0,1,1,1].; 한 방의 사람 수 P일 때 시간 O(P²), 공간 O(P); 방 크기는 5×5 고정
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:19:39
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/053_81302_%EA%B1%B0%EB%A6%AC%EB%91%90%EA%B8%B0_%ED%99%95%EC%9D%B8%ED%95%98%EA%B8%B0/README.md)
