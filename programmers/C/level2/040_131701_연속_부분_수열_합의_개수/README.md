# 연속 부분 수열 합의 개수

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131701) · Level 2 · C

## 풀이

각 시작점에서 원형 인덱스를 나머지 연산으로 돌리며 길이 1~N의 합 누적; 합별 bool 표로 중복 제거
예: [7,9,1,1,4]의 서로 다른 합은 18종류; 전체 합 S에 대해 시간 O(N²+S), 공간 O(S)

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

int solution(int elements[], size_t elements_len) {
    int total_sum = 0;
    for (size_t i = 0; i < elements_len; ++i) total_sum += elements[i];
    bool* seen = calloc((size_t)total_sum + 1, sizeof(*seen)); int answer = 0;
    for (size_t start = 0; start < elements_len; ++start) {
        int total = 0;
        for (size_t len = 0; len < elements_len; ++len) {
            total += elements[(start + len) % elements_len];
            if (!seen[total]) { seen[total] = true; ++answer; }
        }
    }
    free(seen);
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
// int solution(int elements[], size_t elements_len) {  // 각 시작점에서 원형 인덱스를 나머지 연산으로 돌리며 길이 1~N의 합 누적; 합별 bool 표로 중복 제거
//     int total_sum = 0;  // 원형 배열 전체 합 저장
//     for (size_t i = 0; i < elements_len; ++i) total_sum += elements[i];  // 전체 합에 더할 원소 위치 순서대로 확인; 원형 배열 전체 합 / 전체 합에 더할 원소 위치 더해 누적
//     bool* seen = calloc((size_t)total_sum + 1, sizeof(*seen)); int answer = 0;  // 만들어 본 연속 부분합 표시 / 서로 다른 부분합 수 공간 확보하고 0으로 시작
//     for (size_t start = 0; start < elements_len; ++start) {  // 구간의 시작 위치 순서대로 확인
//         int total = 0;  // 현재 원형 구간 합 저장
//         for (size_t len = 0; len < elements_len; ++len) {  // 구간에 추가한 원소 수 순서대로 확인
//             total += elements[(start + len) % elements_len];  // 현재 원형 구간 합 / 구간의 시작 위치 / 구간에 추가한 원소 수 더해 누적
//             if (!seen[total]) { seen[total] = true; ++answer; }  // 처음 만든 구간 합일 때만 표시하고 서로 다른 합 개수 늘리기
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     free(seen);  // 만들어 본 연속 부분합 표시 임시 공간 정리
//     return answer;  // 서로 다른 부분합 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 시작점에서 원형 인덱스를 나머지 연산으로 돌리며 길이 1~N의 합 누적; 합별 bool 표로 중복 제거
// 예: [7,9,1,1,4]의 서로 다른 합은 18종류; 전체 합 S에 대해 시간 O(N²+S), 공간 O(S)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:16:34
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/040_131701_%EC%97%B0%EC%86%8D_%EB%B6%80%EB%B6%84_%EC%88%98%EC%97%B4_%ED%95%A9%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
