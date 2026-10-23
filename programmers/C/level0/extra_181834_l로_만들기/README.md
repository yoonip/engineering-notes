# l로 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181834) · Level 0 · C

## 풀이

입력의 각 소문자를 'l'과 비교. 'a'부터 'k'까지는 'l'로 바꾸고, 'l'부터 'z'까지는 원래 문자를 유지

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* myString) {
    size_t n = strlen(myString);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) answer[i] = myString[i] < 'l' ? 'l' : myString[i];
    answer[n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* myString) {  // l로 만들기 풀이 시작
//     size_t n = strlen(myString);  // 입력 문자열의 문자 수를 strlen으로 구해 n에 저장
//     char* answer = malloc(n + 1);  // 문자 n개와 끝의 널 문자 한 칸을 담을 새 문자열 공간을 할당
//     for (size_t i = 0; i < n; ++i) answer[i] = myString[i] < 'l' ? 'l' : myString[i];  // 각 문자를 'l'과 비교해 앞선 알파벳이면 'l'로 바꾸고, 나머지는 그대로 복사
//     answer[n] = '\0';  // 문자 n개 뒤에 널 문자를 넣어 결과 문자열을 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력의 각 소문자를 'l'과 비교. 'a'부터 'k'까지는 'l'로 바꾸고, 'l'부터 'z'까지는 원래 문자를 유지
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:22:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181834_l%EB%A1%9C_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
