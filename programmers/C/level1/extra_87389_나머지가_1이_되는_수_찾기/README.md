# 나머지가 1이 되는 수 찾기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/87389) · Level 1 · C

## 풀이

2부터 작은 수를 차례대로 확인; n을 나눈 나머지가 처음으로 1이 되는 수를 반환

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

int solution(int n) {
    for (int x = 2; x < n; ++x) if (n % x == 1) return x;
    return n - 1;
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
// int solution(int n) {  // 2부터 작은 수를 차례대로 확인; n을 나눈 나머지가 처음으로 1이 되는 수를 반환
//     for (int x = 2; x < n; ++x) if (n % x == 1) return x;  // 2부터 차례로 나눠 보고 나머지가 1인 첫 수 반환
//     return n - 1;  // 앞에서 못 찾았으면 항상 나머지 1을 만드는 n-1 반환
// }  // 이 범위 끝

// 풀이 요약
// 2부터 작은 수를 차례대로 확인; n을 나눈 나머지가 처음으로 1이 되는 수를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:52:38
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_87389_%EB%82%98%EB%A8%B8%EC%A7%80%EA%B0%80_1%EC%9D%B4_%EB%90%98%EB%8A%94_%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
