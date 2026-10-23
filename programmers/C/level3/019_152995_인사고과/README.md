# 인사고과

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/152995) · Level 3 · C

## 풀이

첫 점수를 내림차순, 같은 첫 점수에서는 둘째 점수를 오름차순으로 정렬; 이 순서면 앞에서 본 둘째 점수보다 낮은 직원만 두 점수 모두 낮은 제외 대상
완호가 제외되면 -1, 아니면 유효 직원 중 점수 합이 완호보다 큰 사람 수+1을 반환; 시간 O(N log N), 공간 O(N)
예: [[2,2],[1,4],[3,2],[3,2],[2,1]]에서 [2,1]만 제외되고, 완호보다 합이 큰 유효 직원 세 명이 있어 4등

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { int first, second; } Score;
static int compare(const void* p, const void* q) {
    const Score* a = p; const Score* b = q;
    if (a->first != b->first) return (b->first > a->first) - (b->first < a->first);
    return (a->second > b->second) - (a->second < b->second);
}
int solution(int** scores, size_t scores_rows, size_t scores_cols) {
    (void)scores_cols; Score target = {scores[0][0],scores[0][1]}; int target_sum = target.first + target.second;
    Score* sorted = malloc(scores_rows * sizeof(*sorted)); for (size_t i = 0; i < scores_rows; ++i) sorted[i] = (Score){scores[i][0],scores[i][1]};
    qsort(sorted, scores_rows, sizeof(*sorted), compare); int answer = 1, best_second = -1;
    for (size_t i = 0; i < scores_rows; ++i) {
        Score current = sorted[i];
        if (current.second < best_second) { if (current.first == target.first && current.second == target.second) { free(sorted); return -1; } continue; }
        best_second = current.second; if (current.first + current.second > target_sum) ++answer;
    }
    free(sorted);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// typedef struct { int first, second; } Score;  // 직원의 두 평가 점수를 한 항목으로 묶기
// static int compare(const void* p, const void* q) {  // 첫 점수 내림차순, 같은 첫 점수는 둘째 점수 오름차순 비교
//     const Score* a = p; const Score* b = q;  // 첫 비교 직원 / 둘째 비교 직원 저장
//     if (a->first != b->first) return (b->first > a->first) - (b->first < a->first);  // 첫 점수가 다르면 내림차순으로 비교
//     return (a->second > b->second) - (a->second < b->second);  // 첫 비교 직원 / 둘째 비교 직원로 최종값 계산
// }  // 이 범위 끝
// int solution(int** scores, size_t scores_rows, size_t scores_cols) {  // 첫 점수를 내림차순, 같은 첫 점수에서는 둘째 점수를 오름차순으로 정렬; 이 순서면 앞에서 본 둘째 점수보다 낮은 직원만 두 점수 모두 낮은 제외 대상
//     (void)scores_cols; Score target = {scores[0][0],scores[0][1]}; int target_sum = target.first + target.second;  // 완호의 두 점수 / 완호의 점수 합 갱신
//     Score* sorted = malloc(scores_rows * sizeof(*sorted)); for (size_t i = 0; i < scores_rows; ++i) sorted[i] = (Score){scores[i][0],scores[i][1]};  // 첫 점수 내림차순 둘째 점수 오름차순 사본 / 직원 정렬 위치 공간 확보
//     qsort(sorted, scores_rows, sizeof(*sorted), compare); int answer = 1, best_second = -1;  // 첫 점수 내림차순 둘째 점수 오름차순 사본 / 완호보다 높은 유효 직원 수에 1을 더한 순위 정렬 순서 맞추기
//     for (size_t i = 0; i < scores_rows; ++i) {  // 직원 정렬 위치 순서대로 확인
//         Score current = sorted[i];  // 현재 비교할 직원 점수 저장
//         if (current.second < best_second) { if (current.first == target.first && current.second == target.second) { free(sorted); return -1; } continue; }  // 앞 사람보다 두 번째 점수가 낮으면 탈락, 원호라면 -1 반환
//         best_second = current.second; if (current.first + current.second > target_sum) ++answer;  // 앞선 직원의 둘째 점수 최댓값 갱신
//     }  // 이 범위 끝
//     free(sorted);  // 첫 점수 내림차순 둘째 점수 오름차순 사본 임시 공간 정리
//     return answer;  // 완호보다 높은 유효 직원 수에 1을 더한 순위 반환
// }  // 이 범위 끝

// 풀이 요약
// 첫 점수를 내림차순, 같은 첫 점수에서는 둘째 점수를 오름차순으로 정렬; 이 순서면 앞에서 본 둘째 점수보다 낮은 직원만 두 점수 모두 낮은 제외 대상
// 완호가 제외되면 -1, 아니면 유효 직원 중 점수 합이 완호보다 큰 사람 수+1을 반환; 시간 O(N log N), 공간 O(N)
// 예: [[2,2],[1,4],[3,2],[3,2],[2,1]]에서 [2,1]만 제외되고, 완호보다 합이 큰 유효 직원 세 명이 있어 4등
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:29:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/019_152995_%EC%9D%B8%EC%82%AC%EA%B3%A0%EA%B3%BC/README.md)
