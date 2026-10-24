# 카운트 다운

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131129) · Level 3 · C

## 풀이

점수를 1부터 target까지 늘리며 마지막 다트의 점수를 모두 비교하는 DP; 우선 다트 수를 최소화하고, 다트 수가 같을 때만 싱글·불을 최대화하기

동일한 점수를 싱글로도 낼 수 있으면 더블·트리플보다 항상 유리하므로 점수별 최선의 종류만 남기기; 서로 다른 점수 수 C≤43에 대해 시간 O(target×C), 공간 O(target)

예: 21은 트리플 7 한 발이라 [1,0]; 58은 불 50+싱글 8 두 발이므로 [2,2]

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int* solution(int target) {
    bool possible[61] = {false};
    for (int i = 1; i <= 20; ++i) possible[i] = possible[2 * i] = possible[3 * i] = true;
    possible[50] = true; int* throws = malloc(((size_t)target + 1) * sizeof(*throws)); int* singles = calloc((size_t)target + 1, sizeof(*singles)); throws[0] = 0;
    for (int total = 1; total <= target; ++total) {
        throws[total] = target + 1;
        for (int score = 1; score <= 60 && score <= total; ++score) if (possible[score]) {
            int count = throws[total - score] + 1, good = singles[total - score] + (score <= 20 || score == 50);
            if (count < throws[total] || (count == throws[total] && good > singles[total])) { throws[total] = count; singles[total] = good; }
        }
    }
    int* answer = malloc(2 * sizeof(*answer)); answer[0] = throws[target]; answer[1] = singles[target]; free(throws); free(singles);
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
// int* solution(int target) {  // 점수를 1부터 target까지 늘리며 마지막 다트의 점수를 모두 비교하는 DP; 우선 다트 수를 최소화하고, 다트 수가 같을 때만 싱글·불을 최대화하기
//     bool possible[61] = {false};  // 한 번 던져 얻을 수 있는 점수 저장
//     for (int i = 1; i <= 20; ++i) possible[i] = possible[2 * i] = possible[3 * i] = true;  // 기본 점수 후보 순서대로 확인; 한 번 던져 얻을 수 있는 점수 갱신
//     possible[50] = true; int* throws = malloc(((size_t)target + 1) * sizeof(*throws)); int* singles = calloc((size_t)target + 1, sizeof(*singles)); throws[0] = 0;  // 한 번 던져 얻을 수 있는 점수 / 점수별 최소 다트 수 / 같은 다트 수에서 최대 싱글과 불 수 공간 확보하고 0으로 시작
//     for (int total = 1; total <= target; ++total) {  // 이번에 채울 누적 점수 순서대로 확인
//         throws[total] = target + 1;  // 점수별 최소 다트 수 갱신
//         for (int score = 1; score <= 60 && score <= total; ++score) if (possible[score]) {  // 한 번에 만들 수 있고 남은 합을 넘지 않는 점수만 선택
//             int count = throws[total - score] + 1, good = singles[total - score] + (score <= 20 || score == 50);  // 이 점수를 쓰는 총 다트 수 / 이 점수를 쓰는 싱글과 불 수 저장
//             if (count < throws[total] || (count == throws[total] && good > singles[total])) { throws[total] = count; singles[total] = good; }  // 던진 수가 적거나 동률에서 싱글·불이 많으면 더 좋은 경로로 교체
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     int* answer = malloc(2 * sizeof(*answer)); answer[0] = throws[target]; answer[1] = singles[target]; free(throws); free(singles);  // 최소 다트 수와 최대 싱글 불 수 공간 확보
//     return answer;  // 최소 다트 수와 최대 싱글 불 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 점수를 1부터 target까지 늘리며 마지막 다트의 점수를 모두 비교하는 DP; 우선 다트 수를 최소화하고, 다트 수가 같을 때만 싱글·불을 최대화하기
// 동일한 점수를 싱글로도 낼 수 있으면 더블·트리플보다 항상 유리하므로 점수별 최선의 종류만 남기기; 서로 다른 점수 수 C≤43에 대해 시간 O(target×C), 공간 O(target)
// 예: 21은 트리플 7 한 발이라 [1,0]; 58은 불 50+싱글 8 두 발이므로 [2,2]
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:31:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/029_131129_%EC%B9%B4%EC%9A%B4%ED%8A%B8_%EB%8B%A4%EC%9A%B4/README.md)
