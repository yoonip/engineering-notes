# 문자열 정렬하기 (2)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120911) · Level 0 · C

## 풀이

각 입력 문자를 소문자로 바꿔 알파벳별 빈도를 세기. a부터 z까지 순서대로 해당 문자를 빈도만큼 출력 배열에 써서 소문자 정렬 결과를 만들기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string) {
    int counts[26] = {0};
    size_t n = strlen(my_string), pos = 0;
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) ++counts[tolower((unsigned char)my_string[i]) - 'a'];
    for (int i = 0; i < 26; ++i) for (int j = 0; j < counts[i]; ++j) answer[pos++] = 'a' + i;
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
// char* solution(const char* my_string) {  // 문자열 정렬하기 (2) 풀이 시작
//     int counts[26] = {0};  // 소문자 a부터 z까지의 등장 횟수를 저장할 counts의 26개 원소를 0으로 초기화
//     size_t n = strlen(my_string), pos = 0;  // 입력 길이 n을 구하고 결과 문자열에 다음 문자를 쓸 위치 pos를 0으로 초기화
//     char* answer = malloc(n + 1);  // 문자 n개와 끝의 널 문자 한 칸을 담을 결과 공간을 할당
//     for (size_t i = 0; i < n; ++i) ++counts[tolower((unsigned char)my_string[i]) - 'a'];  // 각 문자를 unsigned char로 변환해 tolower에 전달하고, 소문자에서 'a'를 뺀 칸의 개수를 늘림
//     for (int i = 0; i < 26; ++i) for (int j = 0; j < counts[i]; ++j) answer[pos++] = 'a' + i;  // 알파벳 번호 i를 작은 순서로 순회하며 그 문자를 counts[i]번 써서 결과를 오름차순으로 만들기
//     answer[pos] = '\0';  // 마지막 문자를 쓴 위치 뒤에 널 문자를 넣어 결과 문자열을 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 입력 문자를 소문자로 바꿔 알파벳별 빈도를 세기. a부터 z까지 순서대로 해당 문자를 빈도만큼 출력 배열에 써서 소문자 정렬 결과를 만들기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:24:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120911_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%A0%95%EB%A0%AC%ED%95%98%EA%B8%B0_%282%29/README.md)
