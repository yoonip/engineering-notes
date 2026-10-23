# 자연수 뒤집어 배열로 만들기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12932) · Level 1 · C

## 풀이

10으로 나눈 나머지를 차례대로 기록하면 십진 자릿수의 역순이 됨

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

int* solution(long long n) {
    long long value = n; size_t length = 0;
    do { ++length; value /= 10; } while (value);
    int* answer = malloc(length * sizeof(int));
    for (size_t i = 0; i < length; ++i) { answer[i] = (int)(n % 10); n /= 10; }
    return answer;
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
// int* solution(long long n) {  // 10으로 나눈 나머지를 차례대로 기록하면 십진 자릿수의 역순이 됨
//     long long value = n; size_t length = 0;  // 자릿수 길이를 셀 사본 / 결과 배열에 필요한 자릿수 저장
//     do { ++length; value /= 10; } while (value);  // 결과 배열에 필요한 자릿수 갱신
//     int* answer = malloc(length * sizeof(int));  // 일의 자리부터 담은 배열 공간 확보
//     for (size_t i = 0; i < length; ++i) { answer[i] = (int)(n % 10); n /= 10; }  // 뒤집은 자릿수의 저장 위치 순서대로 확인; 일의 자리부터 담은 배열 갱신
//     return answer;  // 일의 자리부터 담은 배열 반환
// }  // 이 범위 끝

// 풀이 요약
// 10으로 나눈 나머지를 차례대로 기록하면 십진 자릿수의 역순이 됨
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12932_%EC%9E%90%EC%97%B0%EC%88%98_%EB%92%A4%EC%A7%91%EC%96%B4_%EB%B0%B0%EC%97%B4%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
