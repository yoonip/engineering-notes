# 없는 숫자 더하기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/86051) · Level 1 · C

## 풀이

0부터 9까지의 합 45에서 입력된 숫자들의 합을 빼기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int numbers[], size_t numbers_len) {
    int answer = 45; for (size_t i = 0; i < numbers_len; ++i) answer -= numbers[i]; return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// int solution(int numbers[], size_t numbers_len) {  // 0부터 9까지의 합 45에서 입력된 숫자들의 합을 빼기
//     int answer = 45; for (size_t i = 0; i < numbers_len; ++i) answer -= numbers[i]; return answer;  // 0부터 9의 합에서 나온 숫자를 뺀 값 / 합에서 제외할 입력 숫자 위치 저장
// }  // 이 범위 끝

// 풀이 요약
// 0부터 9까지의 합 45에서 입력된 숫자들의 합을 빼기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:53:15
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_86051_%EC%97%86%EB%8A%94_%EC%88%AB%EC%9E%90_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
