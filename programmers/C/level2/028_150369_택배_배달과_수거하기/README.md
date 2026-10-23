# 택배 배달과 수거하기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150369) · Level 2 · C

## 풀이

먼 집부터 필요한 왕복을 확정하기; 한 왕복에서 배달·수거를 각각 cap개까지 처리하고 남는 용량은 가까운 집에 쓰기
예: 첫 예제는 5번·3번 집까지 왕복해 10+6=16.; 시간 O(N), 추가 공간 O(1)

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

long long solution(int cap, int n, int deliveries[], size_t deliveries_len, int pickups[], size_t pickups_len) {
    (void)deliveries_len; (void)pickups_len;
    long long delivery = 0, pickup = 0, answer = 0;
    for (int i = n - 1; i >= 0; --i) {
        delivery += deliveries[i]; pickup += pickups[i]; long long trips = 0;
        if (delivery > 0) trips = (delivery + cap - 1) / cap;
        if (pickup > trips * cap) trips = (pickup + cap - 1) / cap;
        answer += trips * (i + 1) * 2; delivery -= trips * cap; pickup -= trips * cap;
    }
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
// long long solution(int cap, int n, int deliveries[], size_t deliveries_len, int pickups[], size_t pickups_len) {  // 먼 집부터 필요한 왕복을 확정하기; 한 왕복에서 배달·수거를 각각 cap개까지 처리하고 남는 용량은 가까운 집에 쓰기
//     (void)deliveries_len; (void)pickups_len;  // (void)deliveries_len; (void)pickups_len
//     long long delivery = 0, pickup = 0, answer = 0;  // 현재 위치까지 남은 배달 수요 / 현재 위치까지 남은 수거 수요 / 배달과 수거의 최소 총거리 저장
//     for (int i = n - 1; i >= 0; --i) {  // 먼 곳부터 확인할 집 위치 순서대로 확인
//         delivery += deliveries[i]; pickup += pickups[i]; long long trips = 0;  // 현재 위치까지 남은 배달 수요 / 먼 곳부터 확인할 집 위치 / 현재 위치까지 남은 수거 수요 더해 누적
//         if (delivery > 0) trips = (delivery + cap - 1) / cap;  // 현재 위치까지 남은 배달 수요가 0보다 크면 이번 먼 집까지 필요한 왕복 수 갱신
//         if (pickup > trips * cap) trips = (pickup + cap - 1) / cap;  // 배송 기준 왕복으로 수거량을 감당 못 하면 수거 기준 왕복 수로 늘리기
//         answer += trips * (i + 1) * 2; delivery -= trips * cap; pickup -= trips * cap;  // 배달과 수거의 최소 총거리 / 이번 먼 집까지 필요한 왕복 수 / 먼 곳부터 확인할 집 위치 더해 누적
//     }  // 이 범위 끝
//     return answer;  // 배달과 수거의 최소 총거리 반환
// }  // 이 범위 끝

// 풀이 요약
// 먼 집부터 필요한 왕복을 확정하기; 한 왕복에서 배달·수거를 각각 cap개까지 처리하고 남는 용량은 가까운 집에 쓰기
// 예: 첫 예제는 5번·3번 집까지 왕복해 10+6=16.; 시간 O(N), 추가 공간 O(1)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:13:42
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/028_150369_%ED%83%9D%EB%B0%B0_%EB%B0%B0%EB%8B%AC%EA%B3%BC_%EC%88%98%EA%B1%B0%ED%95%98%EA%B8%B0/README.md)
