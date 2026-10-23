# 다항식 더하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120863) · Level 0 · C

## 풀이

일차 항의 계수와 상수를 따로 합산. 계수 1과 불필요한 0 항을 생략해 가장 짧게 표시

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* polynomial) {
    int coefficient = 0, constant = 0;
    const char* p = polynomial;
    while (*p) {
        if (*p == ' ' || *p == '+') { ++p; continue; }
        int value = 0;
        bool has_number = false;
        while (isdigit((unsigned char)*p)) { value = value * 10 + *p++ - '0'; has_number = true; }
        if (*p == 'x') { coefficient += has_number ? value : 1; ++p; }
        else constant += value;
    }
    char* answer = calloc(64, 1);
    if (coefficient == 1) strcpy(answer, "x");
    else if (coefficient) snprintf(answer, 64, "%dx", coefficient);
    if (constant) {
        size_t pos = strlen(answer);
        snprintf(answer + pos, 64 - pos, coefficient ? " + %d" : "%d", constant);
    }
    if (!answer[0]) strcpy(answer, "0");
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
// char* solution(const char* polynomial) {  // 다항식 더하기 풀이 시작
//     int coefficient = 0, constant = 0;  // x의 계수 합과 상수항 합을 따로 누적
//     const char* p = polynomial;  // 아직 읽지 않은 다항식 부분을 가리킬 포인터 준비
//     while (*p) {  // 문자열 끝까지 항과 연산 기호를 순서대로 읽음
//         if (*p == ' ' || *p == '+') { ++p; continue; }  // 항 사이 공백과 더하기 기호는 건너뛰고 다음 항으로 이동
//         int value = 0;  // 이번 항에서 읽는 숫자는 0부터 조립
//         bool has_number = false;  // x 앞에 계수 숫자가 실제로 있었는지 표시
//         while (isdigit((unsigned char)*p)) { value = value * 10 + *p++ - '0'; has_number = true; }  // 연속 숫자를 십진 정수로 조립하고 계수가 명시됐음을 기록
//         if (*p == 'x') { coefficient += has_number ? value : 1; ++p; }  // x가 붙은 항은 계수에 더하기. 숫자가 생략됐으면 계수 1
//         else constant += value;  // x가 붙지 않은 숫자는 상수항의 합에 추가
//     }  // 블록 끝
//     char* answer = calloc(64, 1);  // calloc은 지정한 개수의 메모리를 확보하고 모든 바이트를 0으로 초기화
//     if (coefficient == 1) strcpy(answer, "x");  // 계수가 1이면 1x 대신 x만 출력
//     else if (coefficient) snprintf(answer, 64, "%dx", coefficient);  // snprintf는 버퍼 크기를 넘지 않게 정수를 지정한 형식의 문자열로 기록
//     if (constant) {  // 상수항이 있을 때만 출력 문자열 뒤에 붙이기
//         size_t pos = strlen(answer);  // 상수항을 이어 붙일 현재 결과 문자열 끝 위치 계산
//         snprintf(answer + pos, 64 - pos, coefficient ? " + %d" : "%d", constant);  // snprintf는 버퍼 크기를 넘지 않게 정수를 지정한 형식의 문자열로 기록
//     }  // 블록 끝
//     if (!answer[0]) strcpy(answer, "0");  // x항과 상수항이 모두 없으면 결과 문자열을 0으로 설정
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 일차 항의 계수와 상수를 따로 합산. 계수 1과 불필요한 0 항을 생략해 가장 짧게 표시
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120863_%EB%8B%A4%ED%95%AD%EC%8B%9D_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
