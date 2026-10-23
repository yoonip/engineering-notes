# 문자열 겹쳐쓰기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181943) · Level 0 · C

## 풀이

시작 위치 s부터 덮어쓸 문자열 길이만큼 교체

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, const char* overwrite_string, int s) {
    char* answer = malloc(strlen(my_string) + 1);
    strcpy(answer, my_string);
    memcpy(answer + s, overwrite_string, strlen(overwrite_string));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, const char* overwrite_string, int s) {  // 문자열 겹쳐쓰기 풀이 시작
//     char* answer = malloc(strlen(my_string) + 1);  // malloc으로 원본 길이와 종료 문자에 필요한 공간을 할당
//     strcpy(answer, my_string);  // strcpy로 종료 문자를 포함한 원본 문자열을 결과 공간에 복사
//     memcpy(answer + s, overwrite_string, strlen(overwrite_string));  // 포인터 덧셈으로 위치 s를 찾아 memcpy로 새 문자열만 덮어쓰기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 시작 위치 s부터 덮어쓸 문자열 길이만큼 교체
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:26:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181943_%EB%AC%B8%EC%9E%90%EC%97%B4_%EA%B2%B9%EC%B3%90%EC%93%B0%EA%B8%B0/README.md)
