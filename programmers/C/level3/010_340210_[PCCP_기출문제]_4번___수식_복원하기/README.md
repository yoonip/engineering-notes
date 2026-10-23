# [PCCP 기출문제] 4번 / 수식 복원하기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/340210) · Level 3 · C

## 풀이

등장한 가장 큰 숫자보다 큰 2~9진법을 후보로 삼고, 이미 결과가 알려진 수식을 모두 만족하는 진법만 남기기
X 수식은 가능한 진법마다 계산한 결과 문자열을 비교; 문자열이 하나로 같으면 그 값, 다르면 ?; 수식 수 E·문자 길이 L에 대해 시간 O(8EL), 공간 O(EL)
예: 1+5는 6진법에서 10, 7~9진법에서 6이므로 ?.; 반면 1+2는 모든 후보 진법에서 3으로 같아 확정됨

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

typedef struct { char a[16], b[16], result[16], op; } Expression;
static int number(const char* text, int base) { int value = 0; while (*text) value = value * base + *text++ - '0'; return value; }
static void encode(int value, int base, char* out) {
    char digits[32]; int length = 0; do { digits[length++] = '0' + value % base; value /= base; } while (value);
    for (int i = 0; i < length; ++i) out[i] = digits[length - 1 - i]; out[length] = '\0';
}
char** solution(const char* expressions[], size_t expressions_len) {
    Expression* parsed = malloc(expressions_len * sizeof(*parsed)); int minimum = 2; bool bases[10] = {false};
    for (size_t i = 0; i < expressions_len; ++i) {
        sscanf(expressions[i], "%15s %c %15s = %15s", parsed[i].a, &parsed[i].op, parsed[i].b, parsed[i].result);
        for (size_t j = 0; expressions[i][j]; ++j) if (expressions[i][j] >= '0' && expressions[i][j] <= '9' && expressions[i][j] - '0' + 1 > minimum) minimum = expressions[i][j] - '0' + 1;
    }
    for (int base = minimum; base <= 9; ++base) {
        bases[base] = true;
        for (size_t i = 0; i < expressions_len; ++i) if (parsed[i].result[0] != 'X') {
            int a = number(parsed[i].a, base), b = number(parsed[i].b, base), expected = number(parsed[i].result, base);
            if ((parsed[i].op == '+' ? a + b : a - b) != expected) { bases[base] = false; break; }
        }
    }
    char** answer = malloc(expressions_len * sizeof(*answer)); size_t count = 0;
    for (size_t i = 0; i < expressions_len; ++i) if (parsed[i].result[0] == 'X') {
        char result[32] = "", candidate[32]; bool ambiguous = false;
        for (int base = minimum; base <= 9; ++base) if (bases[base]) {
            int a = number(parsed[i].a, base), b = number(parsed[i].b, base); encode(parsed[i].op == '+' ? a + b : a - b, base, candidate);
            if (!result[0]) strcpy(result, candidate); else if (strcmp(result, candidate)) ambiguous = true;
        }
        answer[count] = malloc(96); snprintf(answer[count++], 96, "%s %c %s = %s", parsed[i].a, parsed[i].op, parsed[i].b, ambiguous ? "?" : result);
    }
    free(parsed);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// typedef struct { char a[16], b[16], result[16], op; } Expression;  // 첫 피연산자 / 둘째 피연산자 / 복원 결과의 공통 표기를 한 상태로 묶기
// static int number(const char* text, int base) { int value = 0; while (*text) value = value * base + *text++ - '0'; return value; }  // 해당 진법의 숫자 문자열을 정수로 변환
// static void encode(int value, int base, char* out) {  // 정수를 해당 진법의 문자열로 변환
//     char digits[32]; int length = 0; do { digits[length++] = '0' + value % base; value /= base; } while (value);  // 진법으로 나눈 나머지를 역순으로 모아 결과 자릿수 만들기
//     for (int i = 0; i < length; ++i) out[i] = digits[length - 1 - i]; out[length] = '\0';  // 입력 식 또는 출력 자리 순서대로 확인; 문자열 끝에 널 문자 붙이기
// }  // 이 범위 끝
// char** solution(const char* expressions[], size_t expressions_len) {  // 등장한 가장 큰 숫자보다 큰 2~9진법을 후보로 삼고, 이미 결과가 알려진 수식을 모두 만족하는 진법만 남기기
//     Expression* parsed = malloc(expressions_len * sizeof(*parsed)); int minimum = 2; bool bases[10] = {false};  // 피연산자와 연산자를 나눈 식 / 등장 숫자를 표현할 최소 진법 / 확정 식과 모두 맞는 진법 공간 확보
//     for (size_t i = 0; i < expressions_len; ++i) {  // 입력 식 또는 출력 자리 순서대로 확인
//         sscanf(expressions[i], "%15s %c %15s = %15s", parsed[i].a, &parsed[i].op, parsed[i].b, parsed[i].result);  // 입력에서 입력 식 또는 출력 자리 / 피연산자와 연산자를 나눈 식 / 첫 피연산자 / 둘째 피연산자 / 복원 결과의 공통 표기 읽기
//         for (size_t j = 0; expressions[i][j]; ++j) if (expressions[i][j] >= '0' && expressions[i][j] <= '9' && expressions[i][j] - '0' + 1 > minimum) minimum = expressions[i][j] - '0' + 1;  // 식에 나온 모든 숫자보다 큰 값으로 최소 진법 설정
//     }  // 이 범위 끝
//     for (int base = minimum; base <= 9; ++base) {  // 검사할 진법 순서대로 확인
//         bases[base] = true;  // 확정 식과 모두 맞는 진법 갱신
//         for (size_t i = 0; i < expressions_len; ++i) if (parsed[i].result[0] != 'X') {  // 결과가 주어진 식으로 가능한 진법을 걸러내기
//             int a = number(parsed[i].a, base), b = number(parsed[i].b, base), expected = number(parsed[i].result, base);  // 첫 피연산자 / 둘째 피연산자 / 식 오른쪽의 진법 변환 값 저장
//             if ((parsed[i].op == '+' ? a + b : a - b) != expected) { bases[base] = false; break; }  // 주어진 결과와 계산 결과가 다르면 해당 진법 제외
//         }  // 이 범위 끝
//     }  // 이 범위 끝
//     char** answer = malloc(expressions_len * sizeof(*answer)); size_t count = 0;  // 복원한 수식 문자열 목록 / 복원한 식 개수 공간 확보
//     for (size_t i = 0; i < expressions_len; ++i) if (parsed[i].result[0] == 'X') {  // 결과가 X인 식만 복원 대상에 넣기
//         char result[32] = "", candidate[32]; bool ambiguous = false;  // 복원 결과의 공통 표기 / 진법마다 결과 표기가 다른지 여부 저장
//         for (int base = minimum; base <= 9; ++base) if (bases[base]) {  // 모든 알려진 식을 통과한 진법에서만 결과 계산
//             int a = number(parsed[i].a, base), b = number(parsed[i].b, base); encode(parsed[i].op == '+' ? a + b : a - b, base, candidate);  // 첫 피연산자 / 둘째 피연산자 저장
//             if (!result[0]) strcpy(result, candidate); else if (strcmp(result, candidate)) ambiguous = true;  // 첫 결과를 보관하고 진법에 따라 다른 표기가 나오면 미확정 표시
//         }  // 이 범위 끝
//         answer[count] = malloc(96); snprintf(answer[count++], 96, "%s %c %s = %s", parsed[i].a, parsed[i].op, parsed[i].b, ambiguous ? "?" : result);  // 복원한 수식 문자열 목록 공간 확보
//     }  // 이 범위 끝
//     free(parsed);  // 피연산자와 연산자를 나눈 식 임시 공간 정리
//     return answer;  // 복원한 수식 문자열 목록 반환
// }  // 이 범위 끝

// 풀이 요약
// 등장한 가장 큰 숫자보다 큰 2~9진법을 후보로 삼고, 이미 결과가 알려진 수식을 모두 만족하는 진법만 남기기
// X 수식은 가능한 진법마다 계산한 결과 문자열을 비교; 문자열이 하나로 같으면 그 값, 다르면 ?; 수식 수 E·문자 길이 L에 대해 시간 O(8EL), 공간 O(EL)
// 예: 1+5는 6진법에서 10, 7~9진법에서 6이므로 ?.; 반면 1+2는 모든 후보 진법에서 3으로 같아 확정됨
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:26:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/010_340210_%5BPCCP_%EA%B8%B0%EC%B6%9C%EB%AC%B8%EC%A0%9C%5D_4%EB%B2%88___%EC%88%98%EC%8B%9D_%EB%B3%B5%EC%9B%90%ED%95%98%EA%B8%B0/README.md)
