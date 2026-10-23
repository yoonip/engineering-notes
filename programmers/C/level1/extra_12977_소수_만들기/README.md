# 소수 만들기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12977) · Level 1 · C

## 풀이

서로 다른 세 수의 합을 계산; 2부터 제곱근 이하의 약수가 없는 합의 개수를 세기

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

int solution(int nums[], size_t nums_len) {
    int answer = 0;
    for (size_t i = 0; i < nums_len; ++i) for (size_t j = i + 1; j < nums_len; ++j) for (size_t k = j + 1; k < nums_len; ++k) {
        int sum = nums[i] + nums[j] + nums[k]; bool prime = true;
        for (int divisor = 2; divisor * divisor <= sum; ++divisor) if (sum % divisor == 0) { prime = false; break; }
        if (prime) ++answer;
    }
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
// int solution(int nums[], size_t nums_len) {  // 서로 다른 세 수의 합을 계산; 2부터 제곱근 이하의 약수가 없는 합의 개수를 세기
//     int answer = 0;  // 합이 소수가 되는 세 수 조합 수 저장
//     for (size_t i = 0; i < nums_len; ++i) for (size_t j = i + 1; j < nums_len; ++j) for (size_t k = j + 1; k < nums_len; ++k) {  // 서로 다른 세 위치를 i < j < k로 골라 중복 조합 피하기
//         int sum = nums[i] + nums[j] + nums[k]; bool prime = true;  // 고른 세 수의 합 / 현재 합의 소수 여부 저장
//         for (int divisor = 2; divisor * divisor <= sum; ++divisor) if (sum % divisor == 0) { prime = false; break; }  // 제곱근까지 나눠 보고 약수가 하나라도 나오면 소수가 아니므로 중단
//         if (prime) ++answer;  // 현재 합의 소수 여부가 남아 있으면 합이 소수가 되는 세 수 조합 수 갱신
//     }  // 이 범위 끝
//     return answer;  // 합이 소수가 되는 세 수 조합 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 서로 다른 세 수의 합을 계산; 2부터 제곱근 이하의 약수가 없는 합의 개수를 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:55:16
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_12977_%EC%86%8C%EC%88%98_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
