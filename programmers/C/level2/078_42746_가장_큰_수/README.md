# 가장 큰 수

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42746) · Level 2 · C

두 숫자 문자열 a, b를 ab와 ba 순으로 연결해 비교합니다. 더 큰 문자열을 만드는 순서로 정렬하며, 입력 1000 이하에서는 비교 문자열 길이가 일정하게 제한됩니다.

예: [3,30,34,5,9]는 9·5·34·3·30 순으로 연결해 '9534330'입니다. 숫자 N개에 대해 시간은 O(N log N), 공간은 O(N)입니다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

typedef struct { char digits[5]; } Number;
static int compare(const void* p, const void* q) {
    const Number* a = p; const Number* b = q;
    char ab[10], ba[10];
    snprintf(ab, sizeof(ab), "%s%s", a->digits, b->digits);
    snprintf(ba, sizeof(ba), "%s%s", b->digits, a->digits);
    return strcmp(ba, ab);
}
char* solution(int numbers[], size_t numbers_len) {
    Number* parts = malloc(numbers_len * sizeof(*parts));
    for (size_t i = 0; i < numbers_len; ++i) snprintf(parts[i].digits, sizeof(parts[i].digits), "%d", numbers[i]);
    qsort(parts, numbers_len, sizeof(*parts), compare);
    char* answer = malloc(numbers_len * 4 + 1);
    size_t pos = 0;
    if (parts[0].digits[0] == '0') { answer[0] = '0'; pos = 1; }
    else for (size_t i = 0; i < numbers_len; ++i) {
        size_t len = strlen(parts[i].digits);
        memcpy(answer + pos, parts[i].digits, len); pos += len;
    }
    answer[pos] = '\0'; free(parts);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // sqrtl 등 실수 수학 함수의 선언
//
// typedef struct { char digits[5]; } Number;  // 숫자 한 개의 십진수 표현을 한 상태로 묶기
// static int compare(const void* p, const void* q) {  // 두 숫자를 이어 붙인 순서를 비교해 더 큰 조합이 앞으로 오게 정렬
//     const Number* a = p; const Number* b = q;  // void 포인터를 읽기 전용 Number 포인터로 받아 비교 대상에 접근
//     char ab[10], ba[10];  // a 뒤에 b를 붙인 수 / b 뒤에 a를 붙인 수 확인
//     snprintf(ab, sizeof(ab), "%s%s", a->digits, b->digits);  // snprintf로 정수 또는 이어 붙인 문자열을 버퍼 크기에 맞게 기록
//     snprintf(ba, sizeof(ba), "%s%s", b->digits, a->digits);  // snprintf로 정수 또는 이어 붙인 문자열을 버퍼 크기에 맞게 기록
//     return strcmp(ba, ab);  // ba와 ab의 사전순 비교 부호를 반환하여 큰 연결 문자열이 앞에 오도록 정렬
// }  // 이 범위 끝
// char* solution(int numbers[], size_t numbers_len) {  // 두 숫자 문자열 a, b를 ab와 ba 순으로 연결해 비교합니다. 더 큰 문자열을 만드는 순서로 정렬하며, 입력 1000 이하에서는 비교 문자열 길이가 일정하게 제한됩니다.
//     Number* parts = malloc(numbers_len * sizeof(*parts));  // 숫자를 문자열로 바꾼 목록 공간 확보
//     for (size_t i = 0; i < numbers_len; ++i) snprintf(parts[i].digits, sizeof(parts[i].digits), "%d", numbers[i]);  // snprintf로 정수 또는 이어 붙인 문자열을 버퍼 크기에 맞게 기록
//     qsort(parts, numbers_len, sizeof(*parts), compare);  // 숫자를 문자열로 바꾼 목록 정렬 순서 맞추기
//     char* answer = malloc(numbers_len * 4 + 1);  // 이어 붙여 만든 가장 큰 수 공간 확보
//     size_t pos = 0;  // 결과 문자열의 다음 위치 저장
//     if (parts[0].digits[0] == '0') { answer[0] = '0'; pos = 1; }  // 가장 앞 숫자가 0이면 전체가 0이므로 결과는 한 글자 0
//     else for (size_t i = 0; i < numbers_len; ++i) {  // 앞 조건이 아니면 변환하거나 붙일 숫자 위치 갱신
//         size_t len = strlen(parts[i].digits);  // 현재 붙일 숫자 길이 저장
//         memcpy(answer + pos, parts[i].digits, len); pos += len;  // 이어 붙여 만든 가장 큰 수 / 결과 문자열의 다음 위치 / 숫자를 문자열로 바꾼 목록 복사
//     }  // 이 범위 끝
//     answer[pos] = '\0'; free(parts);  // 필요한 결과를 먼저 보관하고 임시 배열 정리
//     return answer;  // 이어 붙여 만든 가장 큰 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 두 숫자 문자열 a, b를 ab와 ba 순으로 연결해 비교합니다. 더 큰 문자열을 만드는 순서로 정렬하며, 입력 1000 이하에서는 비교 문자열 길이가 일정하게 제한됩니다.
// 예: [3,30,34,5,9]는 9·5·34·3·30 순으로 연결해 '9534330'입니다. 숫자 N개에 대해 시간은 O(N log N), 공간은 O(N)입니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:21:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level2/078_42746_%EA%B0%80%EC%9E%A5_%ED%81%B0_%EC%88%98/README.md)
