# 모음 제거

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120849) · Level 0 · C

## 풀이

다섯 모음에 속하지 않은 문자와 공백만 유지

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string) {
    char* answer = malloc(strlen(my_string) + 1);
    size_t pos = 0;
    for (size_t i = 0; my_string[i]; ++i)
        if (strchr("aeiou", my_string[i]) == NULL) answer[pos++] = my_string[i];
    answer[pos] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// char* solution(const char* my_string) {  // 모음 제거 풀이 시작
//     char* answer = malloc(strlen(my_string) + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     size_t pos = 0;  // 다음 문자를 쓸 위치는 0부터 시작
//     for (size_t i = 0; my_string[i]; ++i)  // 모든 문자에 대해 다섯 모음 목록에 포함되는지 검사
//         if (strchr("aeiou", my_string[i]) == NULL) answer[pos++] = my_string[i];  // 모음 목록에 없는 문자만 결과에 남기기
//     answer[pos] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 다섯 모음에 속하지 않은 문자와 공백만 유지
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:44
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120849_%EB%AA%A8%EC%9D%8C_%EC%A0%9C%EA%B1%B0/README.md)
