# 최솟값 만들기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12941) · Level 2 · C

한쪽은 작은 수부터, 다른 쪽은 큰 수부터 짝짓습니다. 큰 수끼리 곱해지는 비용을 줄이는 그리디 풀이입니다.

예: [1,2,4]와 [5,4,4]는 5+8+16=29입니다. a≤b, c≤d이면 ac+bd-(ad+bc)=(b-a)(d-c)≥0이므로 반대 순서가 불리하지 않습니다. 원소 N개에 대해 시간은 O(N log N), 공간은 O(N)입니다.

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
// #include <math.h>  // sqrtl 등 실수 수학 함수의 선언
//
// static int compare(const void* p, const void* q) {  // 두 정수를 오름차순으로 비교
//     int a = *(const int*)p, b = *(const int*)q;  // 비교할 두 원소 주소를 int 포인터로 변환하고 역참조하여 값 읽기
//     return (a > b) - (a < b);  // 두 비교 결과 0 또는 1을 빼서 -1, 0, 1의 비교 부호 반환
// }  // 이 범위 끝
// int solution(int A[], size_t A_len, int B[], size_t B_len) {  // 한쪽은 작은 수부터, 다른 쪽은 큰 수부터 짝짓습니다. 큰 수끼리 곱해지는 비용을 줄이는 그리디 풀이입니다.
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
// 한쪽은 작은 수부터, 다른 쪽은 큰 수부터 짝짓습니다. 큰 수끼리 곱해지는 비용을 줄이는 그리디 풀이입니다.
// 예: [1,2,4]와 [5,4,4]는 5+8+16=29입니다. a≤b, c≤d이면 ac+bd-(ad+bc)=(b-a)(d-c)≥0이므로 반대 순서가 불리하지 않습니다. 원소 N개에 대해 시간은 O(N log N), 공간은 O(N)입니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12941_%EC%B5%9C%EC%86%9F%EA%B0%92_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
