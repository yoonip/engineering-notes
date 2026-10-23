# 조건에 맞게 수열 변환하기 2

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181881) · Level 0 · C

## 풀이

원소마다 규칙을 반복해 더 바뀌지 않을 때까지의 횟수 계산. 원소는 독립적으로 변하므로 그 횟수의 최댓값이 배열 전체의 안정화 시점.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int arr[], size_t arr_len) {
    int longest = 0;
    for (size_t i = 0; i < arr_len; ++i) {
        int value = arr[i], steps = 0;
        while (1) {
            int next = value >= 50 && value % 2 == 0 ? value / 2 : value < 50 && value % 2 ? value * 2 + 1 : value;
            if (next == value) break;
            value = next;
            ++steps;
        }
        if (steps > longest) longest = steps;
    }
    return longest;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int arr[], size_t arr_len) {  // 조건에 맞게 수열 변환하기 2 풀이 시작
//     int longest = 0;  // 가장 오래 걸리는 변환 횟수 저장
//     for (size_t i = 0; i < arr_len; ++i) {  // 각 원소가 더 바뀌지 않을 때까지 필요한 횟수를 따로 계산
//         int value = arr[i], steps = 0;  // 변환 중인 값 value와 이 원소의 변환 횟수 steps 준비
//         while (1) {  // 다음 값이 현재 값과 같아질 때까지 변환 반복
//             int next = value >= 50 && value % 2 == 0 ? value / 2 : value < 50 && value % 2 ? value * 2 + 1 : value;  // 규칙을 한 번 적용한 다음 값 저장
//             if (next == value) break;  // 규칙을 적용해도 값이 같으면 이 원소의 변환 종료
//             value = next;  // 변환한 값을 다음 반복의 입력으로 사용
//             ++steps;  // 실제로 값이 달라진 변환 횟수 증가
//         }  // 블록 끝
//         if (steps > longest) longest = steps;  // 현재 원소가 더 오래 걸렸으면 전체 배열의 안정화 시점 갱신
//     }  // 블록 끝
//     return longest;  // 모든 원소가 고정되기까지 필요한 최대 변환 횟수 반환
// }  // 블록 끝// 풀이 요약
// 원소마다 규칙을 반복해 더 바뀌지 않을 때까지의 횟수 계산. 원소는 독립적으로 변하므로 그 횟수의 최댓값이 배열 전체의 안정화 시점.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:08:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181881_%EC%A1%B0%EA%B1%B4%EC%97%90_%EB%A7%9E%EA%B2%8C_%EC%88%98%EC%97%B4_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0_2/README.md)
