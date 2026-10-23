# A 강조하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181874) · Level 0 · C

## 풀이

모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됨

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* myString) {
    size_t n = strlen(myString);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) {
        char c = tolower((unsigned char)myString[i]);
        answer[i] = c == 'a' ? 'A' : c;
    }
    answer[n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* myString) {  // A 강조하기 풀이 시작
//     size_t n = strlen(myString);  // 변환할 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) {  // 모든 문자를 차례로 변환
//         char c = tolower((unsigned char)myString[i]);  // 현재 문자를 우선 소문자로 통일
//         answer[i] = c == 'a' ? 'A' : c;  // 소문자 a만 대문자 A로 바꾸고 다른 소문자는 그대로 저장
//     }  // 블록 끝
//     answer[n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됨
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:15:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181874_A_%EA%B0%95%EC%A1%B0%ED%95%98%EA%B8%B0/README.md)
