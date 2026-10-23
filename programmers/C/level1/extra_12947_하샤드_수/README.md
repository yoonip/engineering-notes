# 하샤드 수

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12947) · Level 1 · C

## 풀이

십진 자릿수의 합을 계산; 원래 수를 그 합으로 나눈 나머지가 0인지 확인

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

bool solution(int x) {
    int sum = 0; for (int n = x; n; n /= 10) sum += n % 10;
    return x % sum == 0;
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
// bool solution(int x) {  // 십진 자릿수의 합을 계산; 원래 수를 그 합으로 나눈 나머지가 0인지 확인
//     int sum = 0; for (int n = x; n; n /= 10) sum += n % 10;  // 원래 수의 자릿수 합 / 자릿수를 꺼낼 사본 저장
//     return x % sum == 0;  // 하샤드 수인지 확인할 원래 값 / 원래 수의 자릿수 합로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 십진 자릿수의 합을 계산; 원래 수를 그 합으로 나눈 나머지가 0인지 확인
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:56:08
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12947_%ED%95%98%EC%83%A4%EB%93%9C_%EC%88%98/README.md)
