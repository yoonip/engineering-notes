# 외계행성의 나이

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120834) · Level 0 · C

## 풀이

숫자 0~9를 a~j로 대응시켜 각 자릿수를 바꾸기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(int age) {
    char digits[16];
    snprintf(digits, sizeof(digits), "%d", age);
    size_t n = strlen(digits);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) answer[i] = 'a' + digits[i] - '0';
    answer[n] = '\0';
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
// char* solution(int age) {  // 외계행성의 나이 풀이 시작
//     char digits[16];  // 나이를 십진수 문자열로 기록할 버퍼 준비
//     snprintf(digits, sizeof(digits), "%d", age);  // snprintf는 버퍼 크기를 넘지 않게 정수를 지정한 형식의 문자열로 기록
//     size_t n = strlen(digits);  // n에 입력 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) answer[i] = 'a' + digits[i] - '0';  // 숫자 문자에서 0을 빼 0~9로 만든 뒤 a를 더해 a~j 문자로 치환
//     answer[n] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 숫자 0~9를 a~j로 대응시켜 각 자릿수를 바꾸기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120834_%EC%99%B8%EA%B3%84%ED%96%89%EC%84%B1%EC%9D%98_%EB%82%98%EC%9D%B4/README.md)
