# 특정 문자 제거하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120826) · Level 0 · C

## 풀이

대소문자를 구분하여 지정 문자만 모두 제거

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string, const char* letter) {
    char* answer = malloc(strlen(my_string) + 1);
    size_t pos = 0;
    for (size_t i = 0; my_string[i]; ++i)
        if (my_string[i] != letter[0]) answer[pos++] = my_string[i];
    answer[pos] = '\0';
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
// char* solution(const char* my_string, const char* letter) {  // 특정 문자 제거하기 풀이 시작
//     char* answer = malloc(strlen(my_string) + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     size_t pos = 0;  // 다음 문자를 쓸 위치는 0부터 시작
//     for (size_t i = 0; my_string[i]; ++i)  // 원본 문자를 차례로 읽어 삭제할 문자와 비교
//         if (my_string[i] != letter[0]) answer[pos++] = my_string[i];  // 지울 문자와 다를 때만 결과에 복사
//     answer[pos] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 대소문자를 구분하여 지정 문자만 모두 제거
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:51:20
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120826_%ED%8A%B9%EC%A0%95_%EB%AC%B8%EC%9E%90_%EC%A0%9C%EA%B1%B0%ED%95%98%EA%B8%B0/README.md)
