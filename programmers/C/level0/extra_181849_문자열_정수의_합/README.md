# 문자열 정수의 합

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181849) · Level 0 · C

## 풀이

문자열을 하나의 큰 정수로 바꾸지 않고, 각 숫자 문자에서 '0'을 빼 자릿값으로 변환한 뒤 모두 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* num_str) {
    int sum = 0;
    for (size_t i = 0; num_str[i]; ++i) sum += num_str[i] - '0';
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* num_str) {  // 문자열 정수의 합 풀이 시작
//     int sum = 0;  // 각 숫자를 더할 누적 합 sum을 0으로 초기화
//     for (size_t i = 0; num_str[i]; ++i) sum += num_str[i] - '0';  // 널 문자 전까지 순회하며 문자에서 '0'을 빼 숫자 0~9로 바꾼 값을 sum에 더하기
//     return sum;  // 문자열의 모든 자릿수를 더한 sum을 반환
// }  // 블록 끝

// 풀이 요약
// 문자열을 하나의 큰 정수로 바꾸지 않고, 각 숫자 문자에서 '0'을 빼 자릿값으로 변환한 뒤 모두 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:19:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181849_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%A0%95%EC%88%98%EC%9D%98_%ED%95%A9/README.md)
