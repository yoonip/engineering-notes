# 문자열 묶기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181855) · Level 0 · C

## 풀이

문자열의 내용이 아닌 길이를 기준으로 개수를 세고 최댓값을 구하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* strArr[], size_t strArr_len) {
    int counts[31] = {0}, answer = 0;
    for (size_t i = 0; i < strArr_len; ++i) {
        int count = ++counts[strlen(strArr[i])];
        if (count > answer) answer = count;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* strArr[], size_t strArr_len) {  // 문자열 묶기 풀이 시작
//     int counts[31] = {0}, answer = 0;  // 길이별 문자열 수 counts와 가장 큰 그룹 크기 answer를 0으로 초기화
//     for (size_t i = 0; i < strArr_len; ++i) {  // 각 문자열을 길이가 같은 그룹에 합류시킴
//         int count = ++counts[strlen(strArr[i])];  // 현재 문자열 길이의 빈도를 늘리고 증가한 그룹 크기 저장
//         if (count > answer) answer = count;  // 현재 그룹이 가장 크면 최대 그룹 크기 갱신
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 문자열의 내용이 아닌 길이를 기준으로 개수를 세고 최댓값을 구하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:17:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181855_%EB%AC%B8%EC%9E%90%EC%97%B4_%EB%AC%B6%EA%B8%B0/README.md)
