# 삼총사

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/131705) · Level 1 · C

## 풀이

서로 다른 세 인덱스를 오름차순으로 골라 합이 0인지 확인; 인덱스 순서를 고정해 같은 세 사람을 중복으로 세지 않음

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

int solution(int number[], size_t number_len) {
    int answer = 0;
    for (size_t i = 0; i < number_len; ++i) for (size_t j = i + 1; j < number_len; ++j) for (size_t k = j + 1; k < number_len; ++k) if (number[i] + number[j] + number[k] == 0) ++answer;
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
// int solution(int number[], size_t number_len) {  // 서로 다른 세 인덱스를 오름차순으로 골라 합이 0인지 확인; 인덱스 순서를 고정해 같은 세 사람을 중복으로 세지 않음
//     int answer = 0;  // 세 수의 합이 0인 조합 수 저장
//     for (size_t i = 0; i < number_len; ++i) for (size_t j = i + 1; j < number_len; ++j) for (size_t k = j + 1; k < number_len; ++k) if (number[i] + number[j] + number[k] == 0) ++answer;  // 서로 다른 세 위치를 i < j < k로 골라 중복 조합 피하기
//     return answer;  // 세 수의 합이 0인 조합 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 서로 다른 세 인덱스를 오름차순으로 골라 합이 0인지 확인; 인덱스 순서를 고정해 같은 세 사람을 중복으로 세지 않음
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:51:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_131705_%EC%82%BC%EC%B4%9D%EC%82%AC/README.md)
