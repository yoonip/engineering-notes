# 요격 시스템

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181188) · Level 2 · C

## 풀이

끝이 빠른 구간부터 끝 바로 왼쪽에서 요격하기; 다음 구간이 그 위치를 포함하지 않을 때만 새로 발사하기
예: 예제 구간을 끝 순으로 처리하면 3회.; 끝점은 포함하지 않아 start >= end일 때 추가하기; 시간 O(N log N), 정렬 공간 O(N)

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

typedef struct { int start, end; } Interval;
static int compare(const void* p, const void* q) {
    int a = ((const Interval*)p)->end, b = ((const Interval*)q)->end;
    return (a > b) - (a < b);
}
int solution(int** targets, size_t targets_rows, size_t targets_cols) {
    (void)targets_cols;
    Interval* intervals = malloc(targets_rows * sizeof(*intervals));
    for (size_t i = 0; i < targets_rows; ++i) intervals[i] = (Interval){targets[i][0],targets[i][1]};
    qsort(intervals, targets_rows, sizeof(*intervals), compare); int answer = 0, end = -1;
    for (size_t i = 0; i < targets_rows; ++i) if (intervals[i].start >= end) { ++answer; end = intervals[i].end; }
    free(intervals);
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
// typedef struct { int start, end; } Interval;  // 현재 한 발로 묶은 구간의 열린 오른쪽 끝를 한 상태로 묶기
// static int compare(const void* p, const void* q) {  // 오른쪽 끝점이 작은 구간부터 정렬
//     int a = ((const Interval*)p)->end, b = ((const Interval*)q)->end;  // 첫 구간 끝점 / 둘째 구간 끝점 저장
//     return (a > b) - (a < b);  // 첫 구간 끝점 / 둘째 구간 끝점로 최종값 계산
// }  // 이 범위 끝
// int solution(int** targets, size_t targets_rows, size_t targets_cols) {  // 끝이 빠른 구간부터 끝 바로 왼쪽에서 요격하기; 다음 구간이 그 위치를 포함하지 않을 때만 새로 발사하기
//     (void)targets_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     Interval* intervals = malloc(targets_rows * sizeof(*intervals));  // 끝점순으로 정렬할 요격 구간 공간 확보
//     for (size_t i = 0; i < targets_rows; ++i) intervals[i] = (Interval){targets[i][0],targets[i][1]};  // 확인할 표적 구간 순서대로 확인; 끝점순으로 정렬할 요격 구간 갱신
//     qsort(intervals, targets_rows, sizeof(*intervals), compare); int answer = 0, end = -1;  // 끝점순으로 정렬할 요격 구간 / 필요한 요격 미사일 수 정렬 순서 맞추기
//     for (size_t i = 0; i < targets_rows; ++i) if (intervals[i].start >= end) { ++answer; end = intervals[i].end; }  // 새 구간 시작이 기존 열린 끝점 이상이면 별도 미사일을 한 발 추가
//     free(intervals);  // 끝점순으로 정렬할 요격 구간 임시 공간 정리
//     return answer;  // 필요한 요격 미사일 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 끝이 빠른 구간부터 끝 바로 왼쪽에서 요격하기; 다음 구간이 그 위치를 포함하지 않을 때만 새로 발사하기
// 예: 예제 구간을 끝 순으로 처리하면 3회.; 끝점은 포함하지 않아 start >= end일 때 추가하기; 시간 O(N log N), 정렬 공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:09:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/014_181188_%EC%9A%94%EA%B2%A9_%EC%8B%9C%EC%8A%A4%ED%85%9C/README.md)
