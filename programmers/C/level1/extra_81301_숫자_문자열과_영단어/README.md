# 숫자 문자열과 영단어

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/81301) · Level 1 · C

## 풀이

숫자 문자는 그대로 읽고 숫자 영단어는 해당 숫자로 바꾸기; 지금까지 읽은 값에 10을 곱하고 다음 숫자를 더하기

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

int solution(const char* s) {
    const char* words[10] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}; int answer = 0;
    for (size_t i = 0; s[i]; ) {
        if (isdigit((unsigned char)s[i])) answer = answer * 10 + s[i++] - '0';
        else for (int digit = 0; digit < 10; ++digit) if (strncmp(s + i, words[digit], strlen(words[digit])) == 0) { answer = answer * 10 + digit; i += strlen(words[digit]); break; }
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
// int solution(const char* s) {  // 숫자 문자는 그대로 읽고 숫자 영단어는 해당 숫자로 바꾸기; 지금까지 읽은 값에 10을 곱하고 다음 숫자를 더하기
//     const char* words[10] = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"}; int answer = 0;  // 숫자와 영어 이름의 대응표 / 읽은 숫자들을 이어 붙인 값 저장
//     for (size_t i = 0; s[i]; ) {  // 다음 숫자 또는 단어의 시작 순서대로 확인
//         if (isdigit((unsigned char)s[i])) answer = answer * 10 + s[i++] - '0';  // 숫자 문자는 바로 정수 값에 이어 붙이고 다음 문자로 이동
//         else for (int digit = 0; digit < 10; ++digit) if (strncmp(s + i, words[digit], strlen(words[digit])) == 0) { answer = answer * 10 + digit; i += strlen(words[digit]); break; }  // 현재 위치와 맞는 영어 숫자를 찾아 정수에 이어 붙이기
//     }  // 이 범위 끝
//     return answer;  // 읽은 숫자들을 이어 붙인 값 반환
// }  // 이 범위 끝

// 풀이 요약
// 숫자 문자는 그대로 읽고 숫자 영단어는 해당 숫자로 바꾸기; 지금까지 읽은 값에 10을 곱하고 다음 숫자를 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:53:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level1/extra_81301_%EC%88%AB%EC%9E%90_%EB%AC%B8%EC%9E%90%EC%97%B4%EA%B3%BC_%EC%98%81%EB%8B%A8%EC%96%B4/README.md)
