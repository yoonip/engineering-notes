# ad 제거하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181870) · Level 0 · C

## 풀이

ad가 포함되지 않은 문자열만 순서를 유지해 남기기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

static char* copy_text(const char* text) {
    char* result = malloc(strlen(text) + 1);
    strcpy(result, text);
    return result;
}
char** solution(const char* strArr[], size_t strArr_len) {
    size_t length = 0;
    for (size_t i = 0; i < strArr_len; ++i) if (!strstr(strArr[i], "ad")) ++length;
    char** answer = malloc(length * sizeof(char*));
    size_t out = 0;
    for (size_t i = 0; i < strArr_len; ++i) if (!strstr(strArr[i], "ad")) answer[out++] = copy_text(strArr[i]);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// static char* copy_text(const char* text) {  // const char*로 받은 문자열을 복사해 새 포인터를 반환할 보조 함수를 정의
//     char* result = malloc(strlen(text) + 1);  // result를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     strcpy(result, text);  // strcpy로 종료 문자까지 문자열을 목적지에 복사
//     return result;  // 새로 할당해 복사한 문자열의 주소 반환
// }  // 블록 끝
// char** solution(const char* strArr[], size_t strArr_len) {  // ad 제거하기 풀이 시작
//     size_t length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < strArr_len; ++i) if (!strstr(strArr[i], "ad")) ++length;  // ad가 들어 있지 않은 문자열 수를 먼저 세기
//     char** answer = malloc(length * sizeof(char*));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; i < strArr_len; ++i) if (!strstr(strArr[i], "ad")) answer[out++] = copy_text(strArr[i]);  // ad가 없는 문자열만 원래 순서대로 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// ad가 포함되지 않은 문자열만 순서를 유지해 남기기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:16:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181870_ad_%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0/README.md)
