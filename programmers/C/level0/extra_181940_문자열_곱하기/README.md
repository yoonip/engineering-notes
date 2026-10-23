# 문자열 곱하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181940) · Level 0 · C

## 풀이

입력 문자열을 k번 순서대로 이어 붙이기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, int k) {
    size_t n = strlen(my_string);
    char* answer = malloc(n * k + 1);
    for (int i = 0; i < k; ++i) memcpy(answer + n * i, my_string, n);
    answer[n * k] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, int k) {  // 문자열 곱하기 풀이 시작
//     size_t n = strlen(my_string);  // strlen으로 문자열 길이를 구해 size_t형 n에 저장
//     char* answer = malloc(n * k + 1);  // malloc으로 반복한 문자열과 종료 문자 한 개를 담을 공간을 할당
//     for (int i = 0; i < k; ++i) memcpy(answer + n * i, my_string, n);  // for로 반복 위치를 순회하고 memcpy로 각 위치에 원본 문자열을 복사
//     answer[n * k] = '\0';  // 문자열 끝에 널 문자를 넣어 반복 결과를 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 문자열을 k번 순서대로 이어 붙이기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:28:07
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181940_%EB%AC%B8%EC%9E%90%EC%97%B4_%EA%B3%B1%ED%95%98%EA%B8%B0/README.md)
