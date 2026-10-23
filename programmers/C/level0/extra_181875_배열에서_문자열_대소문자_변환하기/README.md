# 배열에서 문자열 대소문자 변환하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181875) · Level 0 · C

## 풀이

0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char** solution(const char* strArr[], size_t strArr_len) {
    char** answer = malloc(strArr_len * sizeof(char*));
    for (size_t i = 0; i < strArr_len; ++i) {
        size_t n = strlen(strArr[i]);
        answer[i] = malloc(n + 1);
        for (size_t j = 0; j < n; ++j) answer[i][j] = i % 2 ? toupper((unsigned char)strArr[i][j]) : tolower((unsigned char)strArr[i][j]);
        answer[i][n] = '\0';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char** solution(const char* strArr[], size_t strArr_len) {  // 배열에서 문자열 대소문자 변환하기 풀이 시작
//     char** answer = malloc(strArr_len * sizeof(char*));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < strArr_len; ++i) {  // 입력 문자열을 배열 인덱스 순서대로 변환
//         size_t n = strlen(strArr[i]);  // 현재 변환할 문자열의 문자 수 저장
//         answer[i] = malloc(n + 1);  // 결과를 저장할 메모리 확보
//         for (size_t j = 0; j < n; ++j) answer[i][j] = i % 2 ? toupper((unsigned char)strArr[i][j]) : tolower((unsigned char)strArr[i][j]);  // 문자열 인덱스가 짝수이면 소문자, 홀수이면 대문자로 각 문자 변환
//         answer[i][n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:15:28
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181875_%EB%B0%B0%EC%97%B4%EC%97%90%EC%84%9C_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%8C%80%EC%86%8C%EB%AC%B8%EC%9E%90_%EB%B3%80%ED%99%98%ED%95%98%EA%B8%B0/README.md)
