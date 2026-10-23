# 뒤에 있는 큰 수 찾기

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/154539) · Level 2 · C

## 풀이

아직 답을 못 찾은 인덱스를 값이 비증가하는 스택에 모으기; 더 큰 값이 나타나면 작은 원소의 답을 확정하기
예: [2,3,3,5]는 [3,5,5,-1].; 같은 수는 큰 수가 아니므로 빼지 않음; 시간·공간 O(N)

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

int* solution(int numbers[], size_t numbers_len) {
    int* answer = malloc(numbers_len * sizeof(*answer)); size_t* stack = malloc(numbers_len * sizeof(*stack)); size_t top = 0;
    for (size_t i = 0; i < numbers_len; ++i) {
        answer[i] = -1;
        while (top && numbers[stack[top - 1]] < numbers[i]) answer[stack[--top]] = numbers[i];
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
// int* solution(int numbers[], size_t numbers_len) {  // 아직 답을 못 찾은 인덱스를 값이 비증가하는 스택에 모으기; 더 큰 값이 나타나면 작은 원소의 답을 확정하기
//     int* answer = malloc(numbers_len * sizeof(*answer)); size_t* stack = malloc(numbers_len * sizeof(*stack)); size_t top = 0;  // 각 원소 뒤의 첫 큰 수 / 아직 큰 수를 못 찾은 위치 / 스택에 남은 위치 수 공간 확보
//     for (size_t i = 0; i < numbers_len; ++i) {  // 새로 들어온 숫자 위치 순서대로 확인
//         answer[i] = -1;  // 각 원소 뒤의 첫 큰 수 갱신
//         while (top && numbers[stack[top - 1]] < numbers[i]) answer[stack[--top]] = numbers[i];  // 현재 수가 스택 위 숫자보다 크면 그 위치의 뒤 큰 수로 확정
//         stack[top++] = i;  // 아직 큰 수를 못 찾은 위치 갱신
//     }  // 이 범위 끝
//     free(stack);  // 아직 큰 수를 못 찾은 위치 임시 공간 정리
//     return answer;  // 각 원소 뒤의 첫 큰 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 아직 답을 못 찾은 인덱스를 값이 비증가하는 스택에 모으기; 더 큰 값이 나타나면 작은 원소의 답을 확정하기
// 예: [2,3,3,5]는 [3,5,5,-1].; 같은 수는 큰 수가 아니므로 빼지 않음; 시간·공간 O(N)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:12:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/025_154539_%EB%92%A4%EC%97%90_%EC%9E%88%EB%8A%94_%ED%81%B0_%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
