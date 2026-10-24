# 쿼드압축 후 개수 세기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68936) · Level 2 · C

## 풀이

영역 값이 모두 같으면 한 개로 세고, 다르면 네 사분면으로 나눠 같은 규칙을 재귀 적용하기

예: 전체가 1인 행렬은 크기와 무관하게 [0,1]; 한 변 N일 때 시간 상한 O(N² log N), 재귀 공간 O(log N)

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

static void compress(int** arr, int row, int col, int size, int* answer) {
    int value = arr[row][col]; bool uniform = true;
    for (int r = row; r < row + size && uniform; ++r)
        for (int c = col; c < col + size; ++c)
            if (arr[r][c] != value) { uniform = false; break; }
    if (uniform) { ++answer[value]; return; }
    int half = size / 2;
    compress(arr, row, col, half, answer); compress(arr, row, col + half, half, answer);
    compress(arr, row + half, col, half, answer); compress(arr, row + half, col + half, half, answer);
}
int* solution(int** arr, size_t arr_rows, size_t arr_cols) {
    (void)arr_cols;
    int* answer = calloc(2, sizeof(*answer));
    compress(arr, 0, 0, (int)arr_rows, answer);
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
// static void compress(int** arr, int row, int col, int size, int* answer) {  // 한 영역이 같으면 압축, 다르면 네 부분으로 분할
//     int value = arr[row][col]; bool uniform = true;  // 영역의 기준 숫자 / 영역이 모두 같은지 여부 저장
//     for (int r = row; r < row + size && uniform; ++r)  // 검사할 행 순서대로 확인
//         for (int c = col; c < col + size; ++c)  // 검사할 열 순서대로 확인
//             if (arr[r][c] != value) { uniform = false; break; }  // 기준 칸과 다른 값이 있으면 한 덩어리로 압축할 수 없음
//     if (uniform) { ++answer[value]; return; }  // 영역이 모두 같은지 여부가 남아 있으면 압축 후 0과 1의 개수 갱신
//     int half = size / 2;  // 나눈 영역의 한 변 저장
//     compress(arr, row, col, half, answer); compress(arr, row, col + half, half, answer);  // 영역을 네 부분으로 나누어 같은 압축 검사를 재귀적으로 적용하기
//     compress(arr, row + half, col, half, answer); compress(arr, row + half, col + half, half, answer);  // 영역을 네 부분으로 나누어 같은 압축 검사를 재귀적으로 적용하기
// }  // 이 범위 끝
// int* solution(int** arr, size_t arr_rows, size_t arr_cols) {  // 영역 값이 모두 같으면 한 개로 세고, 다르면 네 사분면으로 나눠 같은 규칙을 재귀 적용하기
//     (void)arr_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* answer = calloc(2, sizeof(*answer));  // 압축 후 0과 1의 개수 공간 확보하고 0으로 시작
//     compress(arr, 0, 0, (int)arr_rows, answer);  // 영역을 네 부분으로 나누어 같은 압축 검사를 재귀적으로 적용하기
//     return answer;  // 압축 후 0과 1의 개수 반환
// }  // 이 범위 끝

// 풀이 요약
// 영역 값이 모두 같으면 한 개로 세고, 다르면 네 사분면으로 나눠 같은 규칙을 재귀 적용하기
// 예: 전체가 1인 행렬은 크기와 무관하게 [0,1]; 한 변 N일 때 시간 상한 O(N² log N), 재귀 공간 O(log N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:20:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/060_68936_%EC%BF%BC%EB%93%9C%EC%95%95%EC%B6%95_%ED%9B%84_%EA%B0%9C%EC%88%98_%EC%84%B8%EA%B8%B0/README.md)
