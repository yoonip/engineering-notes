# 문자열의 뒤의 n글자

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181910) · Level 0 · C

## 풀이

뒤에서 n번째 위치부터 끝까지 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, int n) {
    char* answer = malloc((size_t)n + 1);
    strcpy(answer, my_string + strlen(my_string) - n);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, int n) {  // 문자열의 뒤의 n글자 풀이 시작
//     char* answer = malloc((size_t)n + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     strcpy(answer, my_string + strlen(my_string) - n);  // 포인터 덧셈으로 뒤에서 n번째 위치를 찾아 strcpy로 끝까지 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 뒤에서 n번째 위치부터 끝까지 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:57:12
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181910_%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%98_%EB%92%A4%EC%9D%98_n%EA%B8%80%EC%9E%90/README.md)
