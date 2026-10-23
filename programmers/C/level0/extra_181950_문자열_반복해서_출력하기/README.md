# 문자열 반복해서 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181950) · Level 0 · C

## 풀이

문자열을 읽은 뒤 반복 횟수만큼 이어서 출력

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    char text[100001];
    int n;
    if (scanf("%100000s %d", text, &n) != 2) return 0;
    for (int i = 0; i < n; ++i) fputs(text, stdout);
    putchar('\n');
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[100001];  // 입력 문자열을 저장할 문자 배열임
//     int n;  // 반복 횟수를 저장
//     if (scanf("%100000s %d", text, &n) != 2) return 0;  // 문자열과 반복 횟수를 읽고 입력 실패 시 종료
//     for (int i = 0; i < n; ++i) fputs(text, stdout);  // for문으로 문자열을 n번 출력
//     putchar('\n');  // 출력 끝에서 줄을 바꾸기
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 문자열을 읽은 뒤 반복 횟수만큼 이어서 출력
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181950_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%B0%98%EB%B3%B5%ED%95%B4%EC%84%9C_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
