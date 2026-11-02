# 풍선 터트리기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68646) · Level 3 · C

## 풀이

자신보다 작은 풍선이 양쪽에 모두 있으면 작은 풍선을 두 번 터뜨려야 하므로 남길 수 없습니다. 왼쪽 또는 오른쪽에서 본 최솟값을 갱신하는 풍선은 남길 수 있습니다.

예를 들어 [9,-1,-5]의 왼쪽 최소 기록은 9·-1·-5이고, 오른쪽 최소 기록은 -5입니다. 중복해서 센 -5를 한 번 빼면 3개입니다.

양쪽에서 최솟값을 갱신하는 원소 수를 더하고 전체 최솟값의 중복 한 개를 뺍니다. 배열 길이 N에 대해 시간은 O(N), 추가 공간은 O(1)입니다.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int a[], size_t a_len) {
    int answer = 0, minimum = INT_MAX;
    for (size_t i = 0; i < a_len; ++i) if (a[i] < minimum) { ++answer; minimum = a[i]; }
    minimum = INT_MAX;
    for (size_t i = a_len; i-- > 0;) if (a[i] < minimum) { ++answer; minimum = a[i]; }
    return answer - 1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int a[], size_t a_len) {  // 자신보다 작은 풍선이 양쪽에 모두 있으면 작은 풍선을 두 번 터뜨려야 하므로 남길 수 없습니다. 왼쪽 또는 오른쪽에서 본 최솟값을 갱신하는 풍선은 남길 수 있습니다.
//     int answer = 0, minimum = INT_MAX;  // 좌우 두 번의 탐색에서 최솟값이 갱신된 횟수와 현재 방향의 최솟값 초기화
//     for (size_t i = 0; i < a_len; ++i) if (a[i] < minimum) { ++answer; minimum = a[i]; }  // 왼쪽부터 본 최솟값을 갱신하는 풍선은 살아남을 수 있음
//     minimum = INT_MAX;  // 한쪽 끝부터 본 최솟값 갱신
//     for (size_t i = a_len; i-- > 0;) if (a[i] < minimum) { ++answer; minimum = a[i]; }  // 오른쪽부터 본 최솟값을 갱신하는 풍선도 살아남을 수 있음
//     return answer - 1;  // 두 방향에서 중복 집계한 전체 최솟값 하나를 빼서 생존 가능한 풍선 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 자신보다 작은 풍선이 양쪽에 모두 있으면 작은 풍선을 두 번 터뜨려야 하므로 남길 수 없습니다. 왼쪽 또는 오른쪽에서 본 최솟값을 갱신하는 풍선은 남길 수 있습니다.
// 예를 들어 [9,-1,-5]의 왼쪽 최소 기록은 9·-1·-5이고, 오른쪽 최소 기록은 -5입니다. 중복해서 센 -5를 한 번 빼면 3개입니다.
// 양쪽에서 최솟값을 갱신하는 원소 수를 더하고 전체 최솟값의 중복 한 개를 뺍니다. 배열 길이 N에 대해 시간은 O(N), 추가 공간은 O(1)입니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:38
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/047_68646_%ED%92%8D%EC%84%A0_%ED%84%B0%ED%8A%B8%EB%A6%AC%EA%B8%B0/README.md)
