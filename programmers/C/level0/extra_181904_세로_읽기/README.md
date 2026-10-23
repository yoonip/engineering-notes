# 세로 읽기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181904) · Level 0 · C

## 풀이

열 번호를 0부터 시작하는 인덱스로 바꾸고 m칸 간격의 문자를 읽기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, int m, int c) {
    size_t n = strlen(my_string), used = 0;
    char* answer = malloc(n + 1);
    for (size_t i = (size_t)(c - 1); i < n; i += m) answer[used++] = my_string[i];
    answer[used] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, int m, int c) {  // 세로 읽기 풀이 시작
//     size_t n = strlen(my_string), used = 0;  // strlen으로 입력 길이를 구하고 결과에 저장한 문자 개수를 0으로 초기화
//     char* answer = malloc(n + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     for (size_t i = (size_t)(c - 1); i < n; i += m) answer[used++] = my_string[i];  // 열 번호를 0부터 시작하는 인덱스로 바꾸고 m씩 이동하며 문자를 저장
//     answer[used] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 열 번호를 0부터 시작하는 인덱스로 바꾸고 m칸 간격의 문자를 읽기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:09:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181904_%EC%84%B8%EB%A1%9C_%EC%9D%BD%EA%B8%B0/README.md)
