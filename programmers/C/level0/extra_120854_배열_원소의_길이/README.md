# 배열 원소의 길이

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120854) · Level 0 · C

## 풀이

입력 문자열과 같은 개수의 정수 칸을 마련하고, 각 문자열의 길이를 원래 순서대로 저장

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(const char* strlist[], size_t strlist_len) {
    int* answer = malloc(strlist_len * sizeof(*answer));
    for (size_t i = 0; i < strlist_len; ++i) answer[i] = (int)strlen(strlist[i]);
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
// int* solution(const char* strlist[], size_t strlist_len) {  // 배열 원소의 길이 풀이 시작
//     int* answer = malloc(strlist_len * sizeof(*answer));  // malloc으로 문자열 개수만큼 int를 저장할 메모리를 할당하고, 그 주소를 answer 포인터에 저장. sizeof(*answer)는 int 한 개의 크기임
//     for (size_t i = 0; i < strlist_len; ++i) answer[i] = (int)strlen(strlist[i]);  // 인덱스 i로 모든 문자열을 순회하며 strlen이 센 문자 수를 int로 변환해 대응하는 answer[i]에 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 문자열과 같은 개수의 정수 칸을 마련하고, 각 문자열의 길이를 원래 순서대로 저장
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:31:17
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120854_%EB%B0%B0%EC%97%B4_%EC%9B%90%EC%86%8C%EC%9D%98_%EA%B8%B8%EC%9D%B4/README.md)
