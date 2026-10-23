# 멀리 뛰기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12914) · Level 2 · C

## 풀이

마지막에 1칸 뛰면 n-1칸까지의 모든 방법, 2칸 뛰면 n-2칸까지의 모든 방법이 있음; 두 경우는 겹치지 않아 더하기
예: f(2)=2,f(3)=3,f(4)=5.; 이전 두 값만 보관하므로 시간 O(N), 공간 O(1)

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

long long solution(int n) {
    int previous = 1, current = 1;
    for (int i = 2; i <= n; ++i) {
        int next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return current;
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
// long long solution(int n) {  // 마지막에 1칸 뛰면 n-1칸까지의 모든 방법, 2칸 뛰면 n-2칸까지의 모든 방법이 있음; 두 경우는 겹치지 않아 더하기
//     int previous = 1, current = 1;  // 두 칸 전까지의 이동 방법 수 / 한 칸 전까지의 이동 방법 수 저장
//     for (int i = 2; i <= n; ++i) {  // 채울 이동 거리 순서대로 확인
//         int next = (previous + current) % 1234567;  // 이번 거리의 이동 방법 수 저장
//         previous = current; current = next;  // 두 칸 전까지의 이동 방법 수 / 한 칸 전까지의 이동 방법 수 갱신
//     }  // 이 범위 끝
//     return current;  // 한 칸 전까지의 이동 방법 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 마지막에 1칸 뛰면 n-1칸까지의 모든 방법, 2칸 뛰면 n-2칸까지의 모든 방법이 있음; 두 경우는 겹치지 않아 더하기
// 예: f(2)=2,f(3)=3,f(4)=5.; 이전 두 값만 보관하므로 시간 O(N), 공간 O(1)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:23:02
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/extra_12914_%EB%A9%80%EB%A6%AC_%EB%9B%B0%EA%B8%B0/README.md)
