# 문자열의 앞의 n글자

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181907) · Level 0 · C

## 풀이

문자열의 앞 n글자를 복사해 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, int n) {
    char* answer = malloc((size_t)n + 1);
    memcpy(answer, my_string, (size_t)n);
    answer[n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, int n) {  // 문자열의 앞의 n글자 풀이 시작
//     char* answer = malloc((size_t)n + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     memcpy(answer, my_string, (size_t)n);  // memcpy로 원본의 앞 n바이트를 결과 공간에 복사
//     answer[n] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열의 앞 n글자를 복사해 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:08:42
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181907_%EB%AC%B8%EC%9E%90%EC%97%B4%EC%9D%98_%EC%95%9E%EC%9D%98_n%EA%B8%80%EC%9E%90/README.md)
