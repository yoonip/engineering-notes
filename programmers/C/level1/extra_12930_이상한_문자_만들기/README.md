# 이상한 문자 만들기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12930) · Level 1 · C

## 풀이

단어 안의 위치가 짝수이면 대문자, 홀수이면 소문자로 바꾸기; 공백을 만나면 단어 위치를 0으로 되돌리기

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

char* solution(const char* s) {
    size_t n = strlen(s); char* answer = malloc(n + 1); int index = 0;
    for (size_t i = 0; i < n; ++i) {
        if (s[i] == ' ') { answer[i] = ' '; index = 0; }
        else { answer[i] = index % 2 ? tolower((unsigned char)s[i]) : toupper((unsigned char)s[i]); ++index; }
    }
    answer[n] = '\0';
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
// char* solution(const char* s) {  // 단어 안의 위치가 짝수이면 대문자, 홀수이면 소문자로 바꾸기; 공백을 만나면 단어 위치를 0으로 되돌리기
//     size_t n = strlen(s); char* answer = malloc(n + 1); int index = 0;  // 전체 문자열 길이 / 단어별 대소문자를 바꾼 문자열 / 현재 단어 안에서의 글자 번호 공간 확보
//     for (size_t i = 0; i < n; ++i) {  // 원문에서 읽을 위치 순서대로 확인
//         if (s[i] == ' ') { answer[i] = ' '; index = 0; }  // 공백은 그대로 복사하고 다음 단어의 글자 번호를 0으로 재설정
//         else { answer[i] = index % 2 ? tolower((unsigned char)s[i]) : toupper((unsigned char)s[i]); ++index; }  // 단어 안 짝수 위치는 대문자, 홀수 위치는 소문자로 바꾸고 위치 늘리기
//     }  // 이 범위 끝
//     answer[n] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 단어별 대소문자를 바꾼 문자열 반환
// }  // 이 범위 끝

// 풀이 요약
// 단어 안의 위치가 짝수이면 대문자, 홀수이면 소문자로 바꾸기; 공백을 만나면 단어 위치를 0으로 되돌리기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:52
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_12930_%EC%9D%B4%EC%83%81%ED%95%9C_%EB%AC%B8%EC%9E%90_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
