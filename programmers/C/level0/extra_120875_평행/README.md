# 평행

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120875) · Level 0 · C

## 풀이

네 점을 두 쌍으로 나누는 세 가지 경우를 확인. 두 직선의 좌표 차이를 교차 곱하여 나눗셈에 따른 실수 오차 없이 기울기를 비교

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int** dots, size_t dots_rows, size_t dots_cols) {
    (void)dots_rows; (void)dots_cols;
    const int pairs[3][4] = {{0,1,2,3}, {0,2,1,3}, {0,3,1,2}};
    for (int i = 0; i < 3; ++i) {
        int a = pairs[i][0], b = pairs[i][1], c = pairs[i][2], d = pairs[i][3];
        long long dx1 = dots[b][0] - dots[a][0], dy1 = dots[b][1] - dots[a][1];
        long long dx2 = dots[d][0] - dots[c][0], dy2 = dots[d][1] - dots[c][1];
        if (dy1 * dx2 == dy2 * dx1) return 1;
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int** dots, size_t dots_rows, size_t dots_cols) {  // 평행 풀이 시작
//     (void)dots_rows; (void)dots_cols;  // 문제에서 점 4개와 좌표 2개가 고정되어 있으므로 전달받은 행·열 길이를 별도 반복 조건에 쓰지 않음을 표시
//     const int pairs[3][4] = {{0,1,2,3}, {0,2,1,3}, {0,3,1,2}};  // const 배열 pairs에 네 점을 중복 없이 두 쌍으로 나누는 세 조합을 저장. 각 행의 앞 두 인덱스와 뒤 두 인덱스가 각각 한 직선을 만들기
//     for (int i = 0; i < 3; ++i) {  // for로 점을 두 쌍으로 나누는 세 조합의 인덱스 i를 순회
//         int a = pairs[i][0], b = pairs[i][1], c = pairs[i][2], d = pairs[i][3];  // 이번 분할에서 첫 직선의 두 점 a·b와 둘째 직선의 두 점 c·d 선택
//         long long dx1 = dots[b][0] - dots[a][0], dy1 = dots[b][1] - dots[a][1];  // 첫 직선의 가로 좌표 차이를 dx1, 세로 좌표 차이를 dy1에 long long으로 저장하여 기울기 비교에 사용
//         long long dx2 = dots[d][0] - dots[c][0], dy2 = dots[d][1] - dots[c][1];  // 둘째 직선의 가로 좌표 차이를 dx2, 세로 좌표 차이를 dy2에 long long으로 저장
//         if (dy1 * dx2 == dy2 * dx1) return 1;  // 기울기를 나누지 않고 교차 곱 dy1 * dx2와 dy2 * dx1을 비교. 같으면 두 직선이 평행하므로 즉시 1을 반환
//     }  // 블록 끝
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝
// 풀이 요약
// 네 점을 두 쌍으로 나누는 세 가지 경우를 확인. 두 직선의 좌표 차이를 교차 곱하여 나눗셈에 따른 실수 오차 없이 기울기를 비교
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:29:27
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120875_%ED%8F%89%ED%96%89/README.md)
