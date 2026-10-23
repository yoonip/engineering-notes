# 배열 만들기 5

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181912) · Level 0 · C

## 풀이

시작 위치 s에서 l글자를 정수로 읽고 k보다 큰 값만 저장

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <stddef.h>

int* solution(const char* intStrs[], size_t intStrs_len, int k, int s, int l) {
    int* answer = malloc((intStrs_len ? intStrs_len : 1) * sizeof(int));
    size_t used = 0;
    for (size_t i = 0; i < intStrs_len; ++i) {
        int value = 0;
        for (int j = 0; j < l; ++j) value = value * 10 + intStrs[i][s + j] - '0';
        if (value > k) answer[used++] = value;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int* solution(const char* intStrs[], size_t intStrs_len, int k, int s, int l) {  // 배열 만들기 5 풀이 시작
//     int* answer = malloc((intStrs_len ? intStrs_len : 1) * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     size_t used = 0;  // 기준 k를 넘어서 결과에 저장한 정수 개수를 0으로 시작
//     for (size_t i = 0; i < intStrs_len; ++i) {  // for로 숫자 문자열 배열의 각 문자열을 순회
//         int value = 0;  // 부분 문자열을 정수로 누적할 변수를 0으로 초기화
//         for (int j = 0; j < l; ++j) value = value * 10 + intStrs[i][s + j] - '0';  // for로 l개의 문자를 순회하고 기존 값의 10배에 현재 숫자를 더해 정수로 읽기
//         if (value > k) answer[used++] = value;  // >로 기준을 초과하는지 검사하고 결과 배열에 저장한 뒤 개수를 늘림
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝// 풀이 요약
// 시작 위치 s에서 l글자를 정수로 읽고 k보다 큰 값만 저장
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:07:11
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181912_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_5/README.md)
