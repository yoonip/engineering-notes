# 접미사 배열

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181909) · Level 0 · C

## 풀이

각 위치에서 시작하는 접미사를 모두 만들고 사전순으로 정렬

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

static int compare_suffix(const void* a, const void* b) {
    return strcmp(*(const char* const*)a, *(const char* const*)b);
}

char** solution(const char* my_string) {
    size_t n = strlen(my_string);
    char** answer = malloc(n * sizeof(char*));
    for (size_t i = 0; i < n; ++i) {
        answer[i] = malloc(n - i + 1);
        strcpy(answer[i], my_string + i);
    }
    qsort(answer, n, sizeof(char*), compare_suffix);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// static int compare_suffix(const void* a, const void* b) {  // static 비교 함수를 정의해 qsort가 전달한 두 원소의 주소를 받기
//     return strcmp(*(const char* const*)a, *(const char* const*)b);  // void 포인터를 문자열 포인터의 주소로 변환한 뒤 역참조하고 strcmp로 사전순을 비교
// }  // 블록 끝
//
// char** solution(const char* my_string) {  // 접미사 배열 풀이 시작
//     size_t n = strlen(my_string);  // strlen으로 문자열의 길이를 구해 size_t형으로 저장
//     char** answer = malloc(n * sizeof(char*));  // malloc으로 접미사 문자열들의 주소를 저장할 포인터 배열을 할당
//     for (size_t i = 0; i < n; ++i) {  // size_t형 인덱스를 for로 증가시키며 각 위치를 차례로 처리
//         answer[i] = malloc(n - i + 1);  // malloc으로 현재 접미사와 널 문자를 저장할 공간을 할당
//         strcpy(answer[i], my_string + i);  // 포인터 덧셈으로 i번째 위치에서 시작하는 접미사를 strcpy로 복사
//     }  // 블록 끝
//     qsort(answer, n, sizeof(char*), compare_suffix);  // qsort에 문자열 비교 함수를 전달해 접미사 포인터 배열을 사전순으로 정렬
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 위치에서 시작하는 접미사를 모두 만들고 사전순으로 정렬
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:08:09
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181909_%EC%A0%91%EB%AF%B8%EC%82%AC_%EB%B0%B0%EC%97%B4/README.md)
