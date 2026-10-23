# 자릿수 더하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120906) · Level 0 · C

## 풀이

n % 10으로 일의 자리 숫자를 합에 더하고, 정수 나눗셈 n / 10으로 처리한 자리를 제거. n이 0이 될 때까지 반복

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int sum = 0;
    while (n) { sum += n % 10; n /= 10; }
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int n) {  // 자릿수 더하기 풀이 시작
//     int sum = 0;  // int 변수 sum을 0으로 초기화하여 지금까지 읽은 자리 숫자의 합을 누적
//     while (n) { sum += n % 10; n /= 10; }  // while은 n이 0이 될 때까지 반복. n % 10으로 일의 자리 숫자를 sum에 더한 뒤, 정수 나눗셈 n /= 10으로 처리한 자리를 제거
//     return sum;  // return으로 모든 자리 숫자를 더한 sum을 반환
// }  // 블록 끝

// 풀이 요약
// n % 10으로 일의 자리 숫자를 합에 더하고, 정수 나눗셈 n / 10으로 처리한 자리를 제거. n이 0이 될 때까지 반복
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:25:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120906_%EC%9E%90%EB%A6%BF%EC%88%98_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
