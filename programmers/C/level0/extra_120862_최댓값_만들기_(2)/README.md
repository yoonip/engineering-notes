# 최댓값 만들기 (2)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120862) · Level 0 · C

## 풀이

서로 다른 두 인덱스를 고르는 모든 조합의 곱을 비교. 최댓값을 INT_MIN으로 시작하므로 음수가 포함되어도 가장 큰 곱을 찾기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int numbers[], size_t numbers_len) {
    int answer = INT_MIN;
    for (size_t i = 0; i < numbers_len; ++i)
        for (size_t j = i + 1; j < numbers_len; ++j)
            if (numbers[i] * numbers[j] > answer) answer = numbers[i] * numbers[j];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int numbers[], size_t numbers_len) {  // 최댓값 만들기 (2) 풀이 시작
//     int answer = INT_MIN;  // int 변수 answer를 INT_MIN으로 초기화하여 첫 번째로 계산한 곱이 음수여도 최댓값 후보로 반영
//     for (size_t i = 0; i < numbers_len; ++i)  // size_t 인덱스 i를 0부터 마지막 원소까지 늘리며 곱에 사용할 첫 번째 원소를 고르기
//         for (size_t j = i + 1; j < numbers_len; ++j)  // j를 i + 1부터 늘려 두 번째 원소를 고르기. 같은 원소를 두 번 쓰거나 같은 쌍을 반대로 중복 검사하지 않음
//             if (numbers[i] * numbers[j] > answer) answer = numbers[i] * numbers[j];  // 선택한 두 원소의 곱이 answer보다 클 때만 대입하여 현재까지의 가장 큰 곱을 갱신
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 서로 다른 두 인덱스를 고르는 모든 조합의 곱을 비교. 최댓값을 INT_MIN으로 시작하므로 음수가 포함되어도 가장 큰 곱을 찾기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:30:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120862_%EC%B5%9C%EB%8C%93%EA%B0%92_%EB%A7%8C%EB%93%A4%EA%B8%B0_%282%29/README.md)
