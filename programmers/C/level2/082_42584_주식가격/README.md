# 주식가격

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42584) · Level 2 · C

## 풀이

가격 하락을 기다리는 시점들을 스택에 모으고, 더 낮은 가격이 오면 해당 시점들의 기간을 확정하기; 끝까지 남으면 마지막 초까지의 기간
예: [1,2,3,2,3]의 3은 1초 뒤 하락해 [4,3,1,1,0].; 시간·공간 O(N)

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

int* solution(int prices[], size_t prices_len) {
    int* answer = malloc(prices_len * sizeof(*answer));
    size_t* stack = malloc(prices_len * sizeof(*stack));
    size_t top = 0;
    for (size_t i = 0; i < prices_len; ++i) {
        answer[i] = (int)(prices_len - i - 1);
        while (top && prices[stack[top - 1]] > prices[i]) {
            size_t previous = stack[--top];
            answer[previous] = (int)(i - previous);
        }
        stack[top++] = i;
    }
    free(stack);
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
// int* solution(int prices[], size_t prices_len) {  // 가격 하락을 기다리는 시점들을 스택에 모으고, 더 낮은 가격이 오면 해당 시점들의 기간을 확정하기; 끝까지 남으면 마지막 초까지의 기간
//     int* answer = malloc(prices_len * sizeof(*answer));  // 각 가격이 떨어지기까지의 시간 공간 확보
//     size_t* stack = malloc(prices_len * sizeof(*stack));  // 아직 하락 시점을 못 찾은 인덱스 공간 확보
//     size_t top = 0;  // 스택에 쌓인 가격 수 저장
//     for (size_t i = 0; i < prices_len; ++i) {  // 현재 시점 순서대로 확인
//         answer[i] = (int)(prices_len - i - 1);  // 각 가격이 떨어지기까지의 시간 갱신
//         while (top && prices[stack[top - 1]] > prices[i]) {  // 현재 가격이 더 낮으면 스택 위 시점의 첫 하락 시간을 확정
//             size_t previous = stack[--top];  // 이번 가격 때문에 하락이 확정된 시점 저장
//             answer[previous] = (int)(i - previous);  // 각 가격이 떨어지기까지의 시간 갱신
//         }  // 이 범위 끝
//         stack[top++] = i;  // 아직 하락 시점을 못 찾은 인덱스 갱신
//     }  // 이 범위 끝
//     free(stack);  // 아직 하락 시점을 못 찾은 인덱스 임시 공간 정리
//     return answer;  // 각 가격이 떨어지기까지의 시간 반환
// }  // 이 범위 끝

// 풀이 요약
// 가격 하락을 기다리는 시점들을 스택에 모으고, 더 낮은 가격이 오면 해당 시점들의 기간을 확정하기; 끝까지 남으면 마지막 초까지의 기간
// 예: [1,2,3,2,3]의 3은 1초 뒤 하락해 [4,3,1,1,0].; 시간·공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:00
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/082_42584_%EC%A3%BC%EC%8B%9D%EA%B0%80%EA%B2%A9/README.md)
