# 스타 수열

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/70130) · Level 3 · C

## 풀이

공통 원소별로 겹치지 않는 유효한 인접 쌍을 왼쪽부터 선택합니다. 각 인접 쌍은 두 숫자를 공통 원소로 삼는 후보에만 영향을 주므로 전체 배열을 한 번 순회합니다.

공통값과 다른 값이 만나는 경계의 인접 쌍만 고려해도 됩니다. 가장 먼저 끝나는 쌍을 고르면 뒤에서 사용할 위치를 최대한 남길 수 있습니다.

예제 3에서는 공통값 0을 포함하는 네 쌍을 만들 수 있어 답이 8입니다. 배열 길이 N에 대해 시간과 공간은 O(N)입니다.

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
    int* pairs = calloc(a_len, sizeof(*pairs)); int* used = malloc(a_len * sizeof(*used));
    for (size_t i = 0; i < a_len; ++i) used[i] = -1;
    int answer = 0;
    for (int i = 0; i + 1 < (int)a_len; ++i) {
        int first = a[i], second = a[i + 1]; if (first == second) continue;
        if (used[first] < i) { ++pairs[first]; used[first] = i + 1; }
        if (used[second] < i) { ++pairs[second]; used[second] = i + 1; }
    }
    for (size_t i = 0; i < a_len; ++i) if (pairs[i] > answer) answer = pairs[i];
    free(pairs); free(used);
    return 2 * answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int a[], size_t a_len) {  // 공통 원소별로 겹치지 않는 유효한 인접 쌍을 왼쪽부터 선택합니다. 각 인접 쌍은 두 숫자를 공통 원소로 삼는 후보에만 영향을 주므로 전체 배열을 한 번 순회합니다.
//     int* pairs = calloc(a_len, sizeof(*pairs)); int* used = malloc(a_len * sizeof(*used));  // 쌍 개수 배열만 calloc으로 0 초기화하고 마지막 사용 위치 배열은 malloc으로 확보
//     for (size_t i = 0; i < a_len; ++i) used[i] = -1;  // 각 숫자를 공통값으로 삼았을 때 마지막 사용 위치를 미사용 값 -1로 초기화
//     int answer = 0;  // 가능한 최대 스타 수열 쌍 수 저장
//     for (int i = 0; i + 1 < (int)a_len; ++i) {  // 인접 쌍의 첫 위치 순서대로 확인
//         int first = a[i], second = a[i + 1]; if (first == second) continue;  // 인접한 첫 숫자 / 인접한 둘째 숫자 저장
//         if (used[first] < i) { ++pairs[first]; used[first] = i + 1; }  // 첫 값이 겹치는 쌍에 아직 쓰이지 않았으면 이 쌍에 사용
//         if (used[second] < i) { ++pairs[second]; used[second] = i + 1; }  // 둘째 값이 겹치는 쌍에 아직 쓰이지 않았으면 이 쌍에 사용
//     }  // 이 범위 끝
//     for (size_t i = 0; i < a_len; ++i) if (pairs[i] > answer) answer = pairs[i];  // 숫자별로 만든 서로 안 겹치는 쌍 수 중 최댓값 선택
//     free(pairs); free(used);  // 숫자별 만들 수 있는 서로 안 겹치는 쌍 수 / 숫자별 마지막 사용 위치 임시 공간 정리
//     return 2 * answer;  // 가능한 최대 스타 수열 쌍 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 공통 원소별로 겹치지 않는 유효한 인접 쌍을 왼쪽부터 선택합니다. 각 인접 쌍은 두 숫자를 공통 원소로 삼는 후보에만 영향을 주므로 전체 배열을 한 번 순회합니다.
// 공통값과 다른 값이 만나는 경계의 인접 쌍만 고려해도 됩니다. 가장 먼저 끝나는 쌍을 고르면 뒤에서 사용할 위치를 최대한 남길 수 있습니다.
// 예제 3에서는 공통값 0을 포함하는 네 쌍을 만들 수 있어 답이 8입니다. 배열 길이 N에 대해 시간과 공간은 O(N)입니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:34:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/046_70130_%EC%8A%A4%ED%83%80_%EC%88%98%EC%97%B4/README.md)
