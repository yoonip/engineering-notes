# 문자열 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181952) · Level 0 · C

## 풀이

입력받은 문자열을 바꾸지 않고 그대로 출력

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>

int main(void) {
    char text[1000001];
    if (scanf("%1000000s", text) != 1) return 0;
    puts(text);
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[1000001];  // 문자열과 종료 문자를 담을 문자 배열을 선언
//     if (scanf("%1000000s", text) != 1) return 0;  // 배열 크기에 맞게 문자열을 읽고 입력 성공 여부를 확인
//     puts(text);  // puts로 입력 문자열과 줄바꿈을 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 입력받은 문자열을 바꾸지 않고 그대로 출력
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:25:47
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181952_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
