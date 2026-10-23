# 수 조작하기 2

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181925) · Level 0 · C

## 풀이

인접한 기록의 차이를 조작 문자 w, s, d, a로 바꾸어 연결

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>
#include <stddef.h>

char* solution(int numLog[], size_t numLog_len) {
    char* answer = malloc(numLog_len);
    for (size_t i = 1; i < numLog_len; ++i) {
        int delta = numLog[i] - numLog[i - 1];
        answer[i - 1] = delta == 1 ? 'w' : delta == -1 ? 's' : delta == 10 ? 'd' : 'a';
    }
    answer[numLog_len - 1] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(int numLog[], size_t numLog_len) {  // 수 조작하기 2 풀이 시작
//     char* answer = malloc(numLog_len);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     for (size_t i = 1; i < numLog_len; ++i) {  // for를 두 번째 원소부터 시작해 직전 기록과의 차이를 계산
//         int delta = numLog[i] - numLog[i - 1];  // []로 인접 기록을 읽어 두 값의 변화량을 구하기
//         answer[i - 1] = delta == 1 ? 'w' : delta == -1 ? 's' : delta == 10 ? 'd' : 'a';  // 중첩 삼항 연산자로 변화량을 조작 문자에 대응시켜 결과 위치에 저장
//     }  // 블록 끝
//     answer[numLog_len - 1] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 인접한 기록의 차이를 조작 문자 w, s, d, a로 바꾸어 연결
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:41:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181925_%EC%88%98_%EC%A1%B0%EC%9E%91%ED%95%98%EA%B8%B0_2/README.md)
