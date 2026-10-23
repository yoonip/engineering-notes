# 숨어있는 숫자의 덧셈 (1)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120851) · Level 0 · C

## 풀이

이 문제는 연속된 숫자도 자릿수 하나씩 따로 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* my_string) {
    int sum = 0;
    for (size_t i = 0; my_string[i]; ++i)
        if (isdigit((unsigned char)my_string[i])) sum += my_string[i] - '0';
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* my_string) {  // 숨어있는 숫자의 덧셈 (1) 풀이 시작
//     int sum = 0;  // 합은 0부터 누적
//     for (size_t i = 0; my_string[i]; ++i)  // 문자열의 각 문자를 왼쪽부터 검사
//         if (isdigit((unsigned char)my_string[i])) sum += my_string[i] - '0';  // 숫자 문자이면 0을 빼 자릿값으로 바꾼 뒤 합산
//     return sum;  // 문자열에서 찾은 모든 숫자 자릿값의 합 반환
// }  // 블록 끝
// 풀이 요약
// 이 문제는 연속된 숫자도 자릿수 하나씩 따로 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:30
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120851_%EC%88%A8%EC%96%B4%EC%9E%88%EB%8A%94_%EC%88%AB%EC%9E%90%EC%9D%98_%EB%8D%A7%EC%85%88_%281%29/README.md)
