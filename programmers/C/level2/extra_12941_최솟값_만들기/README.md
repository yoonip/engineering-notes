# 최솟값 만들기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12941) · Level 2 · C

## 풀이

작은 수와 큰 수를 짝지어야 큰 수끼리 곱해지는 비용을 줄일 수 있음; 한쪽 오름차순·다른 쪽 내림차순인 그리디 풀이
예: [1,2,4]와 [5,4,4]는 5+8+16=29.; a≤b,c≤d이면 ac+bd-(ad+bc)=(b-a)(d-c)≥0; 시간 O(N log N), 공간 O(N)

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

static int compare(const void* p, const void* q) {
    int a = *(const int*)p, b = *(const int*)q;
    return (a > b) - (a < b);
}
int solution(int A[], size_t A_len, int B[], size_t B_len) {
    (void)B_len;
    int* a = malloc(A_len * sizeof(*a));
    int* b = malloc(A_len * sizeof(*b));
    memcpy(a, A, A_len * sizeof(*a)); memcpy(b, B, A_len * sizeof(*b));
    qsort(a, A_len, sizeof(*a), compare); qsort(b, A_len, sizeof(*b), compare);
    int answer = 0;
    for (size_t i = 0; i < A_len; ++i) answer += a[i] * b[A_len - 1 - i];
    free(a); free(b);
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
// static int compare(const void* p, const void* q) {  // 두 정수를 오름차순으로 비교
//     int a = *(const int*)p, b = *(const int*)q;  // A의 오름차순 사본 / B의 오름차순 사본 저장
//     return (a > b) - (a < b);  // A의 오름차순 사본 / B의 오름차순 사본로 최종값 계산
// }  // 이 범위 끝
// int solution(int A[], size_t A_len, int B[], size_t B_len) {  // 작은 수와 큰 수를 짝지어야 큰 수끼리 곱해지는 비용을 줄일 수 있음; 한쪽 오름차순·다른 쪽 내림차순인 그리디 풀이
//     (void)B_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* a = malloc(A_len * sizeof(*a));  // A의 오름차순 사본 공간 확보
//     int* b = malloc(A_len * sizeof(*b));  // B의 오름차순 사본 공간 확보
//     memcpy(a, A, A_len * sizeof(*a)); memcpy(b, B, A_len * sizeof(*b));  // A의 오름차순 사본 / B의 오름차순 사본 복사
//     qsort(a, A_len, sizeof(*a), compare); qsort(b, A_len, sizeof(*b), compare);  // A의 오름차순 사본 / B의 오름차순 사본 정렬 순서 맞추기
//     int answer = 0;  // 짝별 곱의 최소 합 저장
//     for (size_t i = 0; i < A_len; ++i) answer += a[i] * b[A_len - 1 - i];  // 서로 반대 순서로 짝지을 위치 순서대로 확인; 짝별 곱의 최소 합 / A의 오름차순 사본 / 서로 반대 순서로 짝지을 위치 더해 누적
//     free(a); free(b);  // A의 오름차순 사본 / B의 오름차순 사본 임시 공간 정리
//     return answer;  // 짝별 곱의 최소 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 작은 수와 큰 수를 짝지어야 큰 수끼리 곱해지는 비용을 줄일 수 있음; 한쪽 오름차순·다른 쪽 내림차순인 그리디 풀이
// 예: [1,2,4]와 [5,4,4]는 5+8+16=29.; a≤b,c≤d이면 ac+bd-(ad+bc)=(b-a)(d-c)≥0; 시간 O(N log N), 공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12941_%EC%B5%9C%EC%86%9F%EA%B0%92_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
