# 정사각형으로 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181830) · Level 0 · C

## 풀이

행 수와 열 수 중 큰 값을 n으로 정하고 n × n 배열을 0으로 초기화. 원래 존재하는 각 행의 원소만 복사하여 부족한 행이나 열을 0으로 남기기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int** solution(int** arr, size_t arr_rows, size_t arr_cols) {
    size_t n = arr_rows > arr_cols ? arr_rows : arr_cols;
    int** answer = malloc(n * sizeof(int*));
    for (size_t i = 0; i < n; ++i) {
        answer[i] = calloc(n, sizeof(int));
        if (i < arr_rows) memcpy(answer[i], arr[i], arr_cols * sizeof(int));
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int** solution(int** arr, size_t arr_rows, size_t arr_cols) {  // 정사각형으로 만들기 풀이 시작
//     size_t n = arr_rows > arr_cols ? arr_rows : arr_cols;  // 행 수와 열 수 중 큰 값을 새 정사각형의 한 변 길이로 선택
//     int** answer = malloc(n * sizeof(int*));  // 새 배열의 n개 행을 가리킬 포인터 공간을 할당
//     for (size_t i = 0; i < n; ++i) {  // 새 행 번호 i를 0부터 n - 1까지 순회
//         answer[i] = calloc(n, sizeof(int));  // 현재 행의 원소 n개를 calloc으로 할당해 모두 0으로 초기화
//         if (i < arr_rows) memcpy(answer[i], arr[i], arr_cols * sizeof(int));  // 원래 존재한 행이면 arr_cols개 원소를 복사하고, 추가된 열과 행의 0은 그대로 두기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 행 수와 열 수 중 큰 값을 n으로 정하고 n × n 배열을 0으로 초기화. 원래 존재하는 각 행의 원소만 복사하여 부족한 행이나 열을 0으로 남기기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:23:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181830_%EC%A0%95%EC%82%AC%EA%B0%81%ED%98%95%EC%9C%BC%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
