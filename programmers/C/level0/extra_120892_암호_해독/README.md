# 암호 해독

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120892) · Level 0 · C

## 풀이

문자 순번은 1부터지만 인덱스는 0부터이므로 첫 위치에 1을 빼기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* cipher, int code) {
    size_t n = strlen(cipher), pos = 0;
    char* answer = malloc(n / code + 1);
    for (size_t i = code - 1; i < n; i += code) answer[pos++] = cipher[i];
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
// char* solution(const char* cipher, int code) {  // 암호 해독 풀이 시작
//     size_t n = strlen(cipher), pos = 0;  // n에 입력 문자열 길이 저장 · 다음 문자를 쓸 위치는 0부터 시작
//     char* answer = malloc(n / code + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = code - 1; i < n; i += code) answer[pos++] = cipher[i];  // code번째 문자부터 code칸씩 건너뛰며 해독할 문자 복사
//     answer[pos] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자 순번은 1부터지만 인덱스는 0부터이므로 첫 위치에 1을 빼기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:46:11
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120892_%EC%95%94%ED%98%B8_%ED%95%B4%EB%8F%85/README.md)
