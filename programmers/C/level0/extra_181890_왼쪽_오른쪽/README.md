# 왼쪽 오른쪽

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181890) · Level 0 · C

## 풀이

앞에서부터 보다가 l 또는 r을 처음 만나는 즉시 해당 부분을 반환

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
char** solution(const char* str_list[], size_t str_list_len) {
    size_t begin = 0, end = 0;
    for (size_t i = 0; i < str_list_len; ++i) {
        if (strcmp(str_list[i], "l") == 0) { end = i; break; }
        if (strcmp(str_list[i], "r") == 0) { begin = i + 1; end = str_list_len; break; }
    }
    char** answer = malloc((end - begin) * sizeof(char*));
    for (size_t i = begin; i < end; ++i) answer[i - begin] = copy_text(str_list[i]);
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
// char** solution(const char* str_list[], size_t str_list_len) {  // 왼쪽 오른쪽 풀이 시작
//     size_t begin = 0, end = 0;  // 선택한 문자열 구간의 시작·끝을 빈 범위로 초기화
//     for (size_t i = 0; i < str_list_len; ++i) {  // 왼쪽부터 처음 등장하는 l 또는 r 탐색
//         if (strcmp(str_list[i], "l") == 0) { end = i; break; }  // 처음 l을 만나면 그 앞쪽 구간을 선택하고 탐색 종료
//         if (strcmp(str_list[i], "r") == 0) { begin = i + 1; end = str_list_len; break; }  // 처음 r을 만나면 그 뒤쪽 구간을 선택하고 탐색 종료
//     }  // 블록 끝
//     char** answer = malloc((end - begin) * sizeof(char*));  // answer를 저장할 메모리 확보
//     for (size_t i = begin; i < end; ++i) answer[i - begin] = copy_text(str_list[i]);  // 선택한 시작·끝 범위의 문자열을 결과에 차례로 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝// 풀이 요약
// 앞에서부터 보다가 l 또는 r을 처음 만나는 즉시 해당 부분을 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:05:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181890_%EC%99%BC%EC%AA%BD_%EC%98%A4%EB%A5%B8%EC%AA%BD/README.md)
