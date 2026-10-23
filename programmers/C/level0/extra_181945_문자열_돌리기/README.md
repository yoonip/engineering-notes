# 문자열 돌리기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181945) · Level 0 · C

## 풀이

문자열을 앞에서부터 읽으며 문자 하나마다 줄을 바꾸기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    char text[100001];
    if (scanf("%100000s", text) != 1) return 0;
    for (int i = 0; text[i]; ++i) printf("%c\n", text[i]);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[100001];  // 입력 문자열과 종료 문자를 담을 char형 배열을 선언
//     if (scanf("%100000s", text) != 1) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     for (int i = 0; text[i]; ++i) printf("%c\n", text[i]);  // for로 각 문자를 읽고 printf의 %c와 줄바꿈으로 한 줄씩 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열을 앞에서부터 읽으며 문자 하나마다 줄을 바꾸기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:26:21
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181945_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%8F%8C%EB%A6%AC%EA%B8%B0/README.md)
