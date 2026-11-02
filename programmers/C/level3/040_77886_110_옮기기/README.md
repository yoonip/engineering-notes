# 110 옮기기

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/77886) · Level 3 · C

## 풀이

스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤에 모아 넣습니다. 이는 끝에 연속한 1들보다 앞인 위치입니다.

예를 들어 1110에서 110을 빼면 1이 남습니다. 남은 문자열에 0이 없으므로 맨 앞에 110을 넣어 1101을 만듭니다.

남은 0은 앞에 유지하고 110은 끝의 1들 앞에 두면 사전순으로 가장 작아집니다. 전체 글자 수 T에 대해 시간과 반환 문자열을 포함한 공간은 O(T)입니다.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

char** solution(const char* s[], size_t s_len) {
    char** answer = malloc(s_len * sizeof(*answer));
    for (size_t i = 0; i < s_len; ++i) {
        size_t len = strlen(s[i]), top = 0, count = 0; char* stack = malloc(len + 1);
        for (size_t j = 0; j < len; ++j) {
            stack[top++] = s[i][j];
            if (top >= 3 && stack[top - 3] == '1' && stack[top - 2] == '1' && stack[top - 1] == '0') { top -= 3; ++count; }
        }
        size_t position = top; while (position && stack[position - 1] != '0') --position;
        answer[i] = malloc(len + 1); memcpy(answer[i], stack, position);
        for (size_t j = 0; j < count; ++j) memcpy(answer[i] + position + 3 * j, "110", 3);
        memcpy(answer[i] + position + 3 * count, stack + position, top - position); answer[i][len] = '\0'; free(stack);
    }
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
// char** solution(const char* s[], size_t s_len) {  // 스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤에 모아 넣습니다. 이는 끝에 연속한 1들보다 앞인 위치입니다.
//     char** answer = malloc(s_len * sizeof(*answer));  // 110을 옮긴 문자열 목록 공간 확보
//     for (size_t i = 0; i < s_len; ++i) {  // 문자열 번호 순서대로 확인
//         size_t len = strlen(s[i]), top = 0, count = 0; char* stack = malloc(len + 1);  // 현재 문자열 길이 / 110을 빼고 남은 글자 수 / 꺼낸 110 묶음 수 / 110을 제거하는 문자 스택 공간 확보
//         for (size_t j = 0; j < len; ++j) {  // 현재 문자 또는 110 묶음 위치 순서대로 확인
//             stack[top++] = s[i][j];  // 110을 제거하는 문자 스택 갱신
//             if (top >= 3 && stack[top - 3] == '1' && stack[top - 2] == '1' && stack[top - 1] == '0') { top -= 3; ++count; }  // 스택 끝의 110을 제거해 따로 세기
//         }  // 이 범위 끝
//         size_t position = top; while (position && stack[position - 1] != '0') --position;  // 마지막 0 바로 뒤의 삽입 위치 저장
//         answer[i] = malloc(len + 1); memcpy(answer[i], stack, position);  // 널 문자를 포함할 결과 공간을 확보하고 삽입 위치 이전의 문자열 복사
//         for (size_t j = 0; j < count; ++j) memcpy(answer[i] + position + 3 * j, "110", 3);  // 꺼낸 110을 삽입 위치부터 count번 연속 복사
//         memcpy(answer[i] + position + 3 * count, stack + position, top - position); answer[i][len] = '\0'; free(stack);  // 남은 뒷부분을 복사하고 널 문자로 끝낸 뒤 임시 스택 해제
//     }  // 이 범위 끝
//     return answer;  // 110을 옮긴 문자열 목록 반환
// }  // 이 범위 끝

// 풀이 요약
// 스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤에 모아 넣습니다. 이는 끝에 연속한 1들보다 앞인 위치입니다.
// 예를 들어 1110에서 110을 빼면 1이 남습니다. 남은 문자열에 0이 없으므로 맨 앞에 110을 넣어 1101을 만듭니다.
// 남은 0은 앞에 유지하고 110은 끝의 1들 앞에 두면 사전순으로 가장 작아집니다. 전체 글자 수 T에 대해 시간과 반환 문자열을 포함한 공간은 O(T)입니다.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:33:29
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level3/040_77886_110_%EC%98%AE%EA%B8%B0%EA%B8%B0/README.md)
