# 대소문자 바꿔서 출력하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181949) · Level 0 · C

## 풀이

각 문자가 소문자이면 대문자로, 대문자이면 소문자로 바꾸기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    char text[100001];
    if (scanf("%100000s", text) != 1) return 0;
    for (int i = 0; text[i]; ++i) {
        unsigned char c = (unsigned char)text[i];
        putchar(islower(c) ? toupper(c) : tolower(c));
    }
    putchar('\n');
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int main(void) {  // 입력을 읽고 답을 출력할 시작점
//     char text[100001];  // 입력 문자열과 종료 문자를 담을 char형 배열을 선언
//     if (scanf("%100000s", text) != 1) return 0;  // scanf로 입력을 읽고 반환값으로 성공한 항목 수를 확인
//     for (int i = 0; text[i]; ++i) {  // for로 널 문자 직전까지 각 문자의 인덱스를 순회
//         unsigned char c = (unsigned char)text[i];  // 문자 분류 함수에 안전하게 전달하도록 문자를 unsigned char로 변환
//         putchar(islower(c) ? toupper(c) : tolower(c));  // islower와 삼항 연산자로 대소문자 변환을 선택하고 putchar로 출력
//     }  // 블록 끝
//     putchar('\n');  // putchar로 줄바꿈 문자 하나를 출력
//     return 0;  // 0으로 정상 종료
// }  // 블록 끝

// 풀이 요약
// 각 문자가 소문자이면 대문자로, 대문자이면 소문자로 바꾸기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:26:01
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181949_%EB%8C%80%EC%86%8C%EB%AC%B8%EC%9E%90_%EB%B0%94%EA%BF%94%EC%84%9C_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md)
