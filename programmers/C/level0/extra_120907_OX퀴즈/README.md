# OX퀴즈

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120907) · Level 0 · C

## 풀이

각 등식에서 두 정수와 연산자, 적힌 결과를 읽어 왼쪽을 계산. 계산값이 오른쪽 정수와 같으면 O, 다르면 X를 입력 순서대로 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char** solution(const char* quiz[], size_t quiz_len) {
    char** answer = malloc(quiz_len * sizeof(*answer));
    for (size_t i = 0; i < quiz_len; ++i) {
        int a, b, result;
        char operation;
        sscanf(quiz[i], "%d %c %d = %d", &a, &operation, &b, &result);
        int actual = operation == '+' ? a + b : a - b;
        answer[i] = malloc(2);
        answer[i][0] = actual == result ? 'O' : 'X'; answer[i][1] = '\0';
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// char** solution(const char* quiz[], size_t quiz_len) {  // OX퀴즈 풀이 시작
//     char** answer = malloc(quiz_len * sizeof(*answer));  // malloc으로 등식 개수만큼 char*를 저장할 공간을 확보. sizeof(*answer)는 문자열 포인터 한 개의 크기임
//     for (size_t i = 0; i < quiz_len; ++i) {  // for로 등식 인덱스 i를 0부터 quiz_len - 1까지 순서대로 처리
//         int a, b, result;  // int 변수 a와 b는 등식 왼쪽의 두 정수이며, result는 등식 오른쪽에 적힌 정수임
//         char operation;  // char 변수 operation에 덧셈 또는 뺄셈 연산자 한 글자를 저장
//         sscanf(quiz[i], "%d %c %d = %d", &a, &operation, &b, &result);  // sscanf로 quiz[i]에서 두 피연산자, 연산자, 오른쪽 결과를 읽기. &는 각 변수에 값을 기록할 주소를 전달
//         int actual = operation == '+' ? a + b : a - b;  // 삼항 연산자 ?:로 operation이 +이면 a + b, 그렇지 않으면 a - b를 계산하여 actual에 저장
//         answer[i] = malloc(2);  // 판정 문자 한 개와 문자열 종료 문자 한 개를 담도록 현재 결과 문자열에 2바이트를 확보
//         answer[i][0] = actual == result ? 'O' : 'X'; answer[i][1] = '\0';  // 실제 계산값 actual과 result가 같으면 O, 다르면 X를 첫 칸에 기록하고, 두 번째 칸에 널 문자를 넣어 문자열을 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 등식에서 두 정수와 연산자, 적힌 결과를 읽어 왼쪽을 계산. 계산값이 오른쪽 정수와 같으면 O, 다르면 X를 입력 순서대로 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:25:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120907_OX%ED%80%B4%EC%A6%88/README.md)
