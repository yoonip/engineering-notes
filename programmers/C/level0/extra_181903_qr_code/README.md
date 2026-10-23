# qr code

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181903) · Level 0 · C

## 풀이

인덱스를 q로 나눈 나머지가 r인 위치의 문자만 연결

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <string.h>

char* solution(int q, int r, const char* code) {
    size_t n = strlen(code), used = 0;
    char* answer = malloc(n + 1);
    for (size_t i = (size_t)r; i < n; i += q) answer[used++] = code[i];
    answer[used] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(int q, int r, const char* code) {  // qr code 풀이 시작
//     size_t n = strlen(code), used = 0;  // strlen으로 입력 길이를 구하고 결과에 저장한 문자 개수를 0으로 초기화
//     char* answer = malloc(n + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     for (size_t i = (size_t)r; i < n; i += q) answer[used++] = code[i];  // for로 r부터 q씩 이동하며 나머지가 r인 인덱스의 문자를 저장
//     answer[used] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 인덱스를 q로 나눈 나머지가 r인 위치의 문자만 연결
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:59:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181903_qr_code/README.md)
