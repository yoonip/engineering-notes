# 배열 만들기 3

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181895) · Level 0 · C

## 풀이

두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙이기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int** intervals, size_t intervals_rows, size_t intervals_cols) {
    int length = intervals[0][1] - intervals[0][0] + intervals[1][1] - intervals[1][0] + 2;
    int* answer = malloc(length * sizeof(int));
    int out = 0;
    for (int r = 0; r < 2; ++r)
        for (int i = intervals[r][0]; i <= intervals[r][1]; ++i) answer[out++] = arr[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int** intervals, size_t intervals_rows, size_t intervals_cols) {  // 배열 만들기 3 풀이 시작
//     int length = intervals[0][1] - intervals[0][0] + intervals[1][1] - intervals[1][0] + 2;  // 결과의 원소 수 저장
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     int out = 0;  // 다음 결과를 기록할 위치 저장
//     for (int r = 0; r < 2; ++r)  // 이어 붙일 두 구간을 주어진 순서대로 선택
//         for (int i = intervals[r][0]; i <= intervals[r][1]; ++i) answer[out++] = arr[i];  // 지정된 두 구간을 양 끝 포함해서 주어진 순서대로 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙이기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:04:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181895_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_3/README.md)
