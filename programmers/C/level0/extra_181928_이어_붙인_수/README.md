# 이어 붙인 수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181928) · Level 0 · C

## 풀이

홀수와 짝수를 각각 원래 순서대로 이어 붙인 정수 두 개를 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stddef.h>

int solution(int num_list[], size_t num_list_len) {
    int odd = 0, even = 0;
    for (size_t i = 0; i < num_list_len; ++i) {
        if (num_list[i] % 2) odd = odd * 10 + num_list[i];
        else even = even * 10 + num_list[i];
    }
    return odd + even;
}

// 전체 코드 줄별 설명
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int solution(int num_list[], size_t num_list_len) {  // 이어 붙인 수 풀이 시작
//     int odd = 0, even = 0;  // 홀수와 짝수를 이어 붙인 결과를 각각 0으로 초기화
//     for (size_t i = 0; i < num_list_len; ++i) {  // for로 정수 목록의 인덱스를 처음부터 끝까지 순회
//         if (num_list[i] % 2) odd = odd * 10 + num_list[i];  // 나머지 연산자 %로 홀수를 골라 기존 수를 10배 한 뒤 마지막 자릿수로 붙이기
//         else even = even * 10 + num_list[i];  // else에서 짝수를 골라 기존 수를 10배 한 뒤 마지막 자릿수로 붙이기
//     }  // 블록 끝
//     return odd + even;  // 홀수끼리 연결한 수와 짝수끼리 연결한 수의 합을 반환
// }  // 블록 끝

// 풀이 요약
// 홀수와 짝수를 각각 원래 순서대로 이어 붙인 정수 두 개를 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:39:10
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181928_%EC%9D%B4%EC%96%B4_%EB%B6%99%EC%9D%B8_%EC%88%98/README.md)
