# 문자열 잘라서 정렬하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181866) · Level 0 · C

## 풀이

x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

static int compare_text(const void* a, const void* b) {
    return strcmp(*(const char* const*)a, *(const char* const*)b);
}
char** solution(const char* myString) {
    size_t count = 0;
    for (size_t i = 0; myString[i]; ) {
        while (myString[i] == 'x') ++i;
        if (!myString[i]) break;
        ++count;
        while (myString[i] && myString[i] != 'x') ++i;
    }
    char** answer = malloc(count * sizeof(char*));
    size_t out = 0;
    for (size_t i = 0; myString[i]; ) {
        while (myString[i] == 'x') ++i;
        if (!myString[i]) break;
        size_t start = i;
        while (myString[i] && myString[i] != 'x') ++i;
        size_t n = i - start;
        answer[out] = malloc(n + 1);
        memcpy(answer[out], myString + start, n);
        answer[out++][n] = '\0';
    }
    qsort(answer, count, sizeof(char*), compare_text);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// static int compare_text(const void* a, const void* b) {  // qsort가 문자열의 사전순을 비교할 때 호출할 보조 함수를 정의
//     return strcmp(*(const char* const*)a, *(const char* const*)b);  // strcmp의 음수·0·양수 결과로 문자열의 사전순을 알립니다
// }  // 블록 끝
// char** solution(const char* myString) {  // 문자열 잘라서 정렬하기 풀이 시작
//     size_t count = 0;  // x 사이에 남길 빈칸 아닌 문자열 조각 수를 0으로 시작
//     for (size_t i = 0; myString[i]; ) {  // 문자열 끝까지 x 사이의 조각 경계를 탐색
//         while (myString[i] == 'x') ++i;  // 연속된 x를 모두 건너뛰어 빈 조각 제외
//         if (!myString[i]) break;  // x를 건너뛴 뒤 문자열이 끝나면 탐색 종료
//         ++count;  // 새로 찾은 빈칸 아닌 조각을 하나 셈
//         while (myString[i] && myString[i] != 'x') ++i;  // 다음 x 또는 문자열 끝까지 현재 조각의 끝 탐색
//     }  // 블록 끝
//     char** answer = malloc(count * sizeof(char*));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; myString[i]; ) {  // 문자열 끝까지 x 사이의 조각 경계를 탐색
//         while (myString[i] == 'x') ++i;  // 연속된 x를 모두 건너뛰어 빈 조각 제외
//         if (!myString[i]) break;  // x를 건너뛴 뒤 문자열이 끝나면 탐색 종료
//         size_t start = i;  // x로 구분된 이번 조각의 시작 위치
//         while (myString[i] && myString[i] != 'x') ++i;  // 다음 x 또는 문자열 끝까지 현재 조각의 끝 탐색
//         size_t n = i - start;  // 현재 문자열 조각의 길이 계산
//         answer[out] = malloc(n + 1);  // 결과를 저장할 메모리 확보
//         memcpy(answer[out], myString + start, n);  // 조각 시작점부터 n글자를 별도 결과 버퍼에 복사
//         answer[out++][n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     }  // 블록 끝
//     qsort(answer, count, sizeof(char*), compare_text);  // qsort와 비교 함수를 사용해 원소를 오름차순으로 정렬
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:16:48
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181866_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%9E%98%EB%9D%BC%EC%84%9C_%EC%A0%95%EB%A0%AC%ED%95%98%EA%B8%B0/README.md)
