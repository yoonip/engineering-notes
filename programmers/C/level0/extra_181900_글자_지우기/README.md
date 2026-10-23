# 글자 지우기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181900) · Level 0 · C

## 풀이

지울 인덱스를 표시한 뒤 남은 문자를 원래 순서대로 연결

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>
#include <stddef.h>

char* solution(const char* my_string, int indices[], size_t indices_len) {
    size_t n = strlen(my_string), used = 0;
    char* answer = malloc(n + 1);
    unsigned char* removed = calloc(n, 1);
    for (size_t i = 0; i < indices_len; ++i) removed[indices[i]] = 1;
    for (size_t i = 0; i < n; ++i) if (!removed[i]) answer[used++] = my_string[i];
    answer[used] = '\0';
    free(removed);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(const char* my_string, int indices[], size_t indices_len) {  // 글자 지우기 풀이 시작
//     size_t n = strlen(my_string), used = 0;  // strlen으로 입력 길이를 구하고 결과에 저장한 문자 개수를 0으로 초기화
//     char* answer = malloc(n + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     unsigned char* removed = calloc(n, 1);  // calloc으로 문자별 삭제 표시 공간을 만들고 모든 바이트를 0으로 초기화
//     for (size_t i = 0; i < indices_len; ++i) removed[indices[i]] = 1;  // for로 삭제 인덱스를 순회하며 해당 위치의 표시를 1로 바꾸기
//     for (size_t i = 0; i < n; ++i) if (!removed[i]) answer[used++] = my_string[i];  // for와 if로 삭제 표시가 없는 문자만 선택해 순서대로 저장
//     answer[used] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     free(removed);  // free로 더 이상 필요하지 않은 삭제 표시 배열의 할당을 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 지울 인덱스를 표시한 뒤 남은 문자를 원래 순서대로 연결
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:02:19
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181900_%EA%B8%80%EC%9E%90_%EC%A7%80%EC%9A%B0%EA%B8%B0/README.md)
