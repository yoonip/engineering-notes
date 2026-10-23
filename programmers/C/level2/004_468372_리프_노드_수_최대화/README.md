# 리프 노드 수 최대화

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/468372) · Level 2 · C

## 풀이

이진 분기 앞부분과 삼진 분기 뒷부분으로 구성한 후보를 비교
이진 깊이를 순회하고, 비용 제한을 넘는 경계의 양쪽을 이진 탐색으로 확인
이진 분기는 리프를 1개, 삼진 분기는 2개 늘리기; 예: 분기 없이 1개, 삼진 분기 한 번이면 3개

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

static long long binary_cost(long long count, int depth) {
    long long total = 0;
    for (int i = 0; i < depth; ++i) { total += count; count = (count + 1) / 2; }
    return total;
}
int solution(int dist_limit, int split_limit) {
    long long answer = 1, width = 1; int depth = 0;
    while (width <= split_limit) {
        long long candidate = width < dist_limit + 1 ? width : dist_limit + 1;
        if (candidate > answer) answer = candidate;
        long long power = 1;
        while (power <= split_limit / width / 3) power *= 3;
        if (!depth) {
            long long ternary = (power - 1) / 2; if (ternary > dist_limit) ternary = dist_limit;
            candidate = 1 + 2 * ternary; if (candidate > answer) answer = candidate;
        } else if (power > 1) {
            long long low = 1, high = width / 2;
            while (low < high) {
                long long mid = low + (high - low) / 2, needed = binary_cost(mid, depth) + mid * (power - 1);
                if (needed >= dist_limit) high = mid; else low = mid + 1;
            }
            for (long long count = low - 1; count <= low; ++count) if (count > 0) {
                long long used = binary_cost(count, depth);
                if (used <= dist_limit) {
                    long long ternary = count * (power - 1); if (ternary > dist_limit - used) ternary = dist_limit - used;
                    candidate = 1 + used + 2 * ternary; if (candidate > answer) answer = candidate;
                }
            }
        }
        if (width > split_limit / 2) break;
        width *= 2; ++depth;
    }
    return (int)answer;
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
// static long long binary_cost(long long count, int depth) {  // 이진 분기 층마다 필요한 거리 더하기
//     long long total = 0;  // 깊이별 필요한 거리 합 저장
//     for (int i = 0; i < depth; ++i) { total += count; count = (count + 1) / 2; }  // 거리를 더할 깊이 순서대로 확인; 깊이별 필요한 거리 합 / 분배할 이진 가지 수 더해 누적
//     return total;  // 깊이별 필요한 거리 합 반환
// }  // 이 범위 끝
// int solution(int dist_limit, int split_limit) {  // 이진 분기 앞부분과 삼진 분기 뒷부분으로 구성한 후보를 비교
//     long long answer = 1, width = 1; int depth = 0;  // 가능한 최대 리프 수 / 현재 이진 단계의 가지 폭 / 이진 분기 깊이 저장
//     while (width <= split_limit) {  // 가지 폭이 분기 한도를 넘지 않는 이진 단계만 검사
//         long long candidate = width < dist_limit + 1 ? width : dist_limit + 1;  // 이번 구조로 얻는 리프 수 저장
//         if (candidate > answer) answer = candidate;  // 이번 분기 구조의 리프 수가 더 크면 최댓값 교체
//         long long power = 1;  // 추가 삼진 분기 배수 저장
//         while (power <= split_limit / width / 3) power *= 3;  // 분기 한도 안에서 가능한 가장 큰 3의 거듭제곱 배수 찾기
//         if (!depth) {  // 이진 분기 깊이가 없으면 처리
//             long long ternary = (power - 1) / 2; if (ternary > dist_limit) ternary = dist_limit;  // 남은 거리로 쓸 삼진 분기 수 저장
//             candidate = 1 + 2 * ternary; if (candidate > answer) answer = candidate;  // 이번 구조로 얻는 리프 수 / 가능한 최대 리프 수 갱신
//         } else if (power > 1) {  // 그 외에는 추가 삼진 분기 배수가 1보다 크면 처리
//             long long low = 1, high = width / 2;  // 삼진 분기를 시작할 가지 수 하한 / 가지 수 상한 저장
//             while (low < high) {  // 이분 탐색 범위가 한 값으로 좁혀질 때까지 중간값의 가능 여부를 확인
//                 long long mid = low + (high - low) / 2, needed = binary_cost(mid, depth) + mid * (power - 1);  // 시험할 가지 수 / 현재 이진과 삼진 구조의 총거리 저장
//                 if (needed >= dist_limit) high = mid; else low = mid + 1;  // 필요 거리가 제한 이상이면 가지 수 상한을 줄이고 아니면 하한 올리기
//             }  // 이 범위 끝
//             for (long long count = low - 1; count <= low; ++count) if (count > 0) {  // 분배할 이진 가지 수 순서대로 확인; 분배할 이진 가지 수가 0보다 크면
//                 long long used = binary_cost(count, depth);  // 먼저 필요한 이진 구조 거리 저장
//                 if (used <= dist_limit) {  // 이진 분기만으로 필요한 거리가 제한 안이면 삼진 분기 추가 검토
//                     long long ternary = count * (power - 1); if (ternary > dist_limit - used) ternary = dist_limit - used;  // 남은 거리로 쓸 삼진 분기 수 저장
//                     candidate = 1 + used + 2 * ternary; if (candidate > answer) answer = candidate;  // 이번 구조로 얻는 리프 수 / 가능한 최대 리프 수 갱신
//                 }  // 이 범위 끝
//             }  // 이 범위 끝
//         }  // 이 범위 끝
//         if (width > split_limit / 2) break;  // 다음에 폭을 두 배로 하면 한도를 넘으므로 이진 단계 탐색 종료
//         width *= 2; ++depth;  // 다음 이진 단계로 가면서 가지 폭을 두 배로, 깊이를 1 증가
//     }  // 이 범위 끝
//     return (int)answer;  // 가능한 최대 리프 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 이진 분기 앞부분과 삼진 분기 뒷부분으로 구성한 후보를 비교
// 이진 깊이를 순회하고, 비용 제한을 넘는 경계의 양쪽을 이진 탐색으로 확인
// 이진 분기는 리프를 1개, 삼진 분기는 2개 늘리기; 예: 분기 없이 1개, 삼진 분기 한 번이면 3개
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:06:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/004_468372_%EB%A6%AC%ED%94%84_%EB%85%B8%EB%93%9C_%EC%88%98_%EC%B5%9C%EB%8C%80%ED%99%94/README.md)
