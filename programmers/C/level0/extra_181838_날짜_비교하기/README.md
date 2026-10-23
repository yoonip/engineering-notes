# 날짜 비교하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181838) · Level 0 · C

## 풀이

연도부터 월, 일 순서로 비교. 처음 다른 항목에서 첫 날짜의 값이 더 작아야 이른 날짜이며, 모든 항목이 같으면 0임

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int date1[], size_t date1_len, int date2[], size_t date2_len) {
    for (int i = 0; i < 3; ++i) if (date1[i] != date2[i]) return date1[i] < date2[i];
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int date1[], size_t date1_len, int date2[], size_t date2_len) {  // 날짜 비교하기 풀이 시작
//     for (int i = 0; i < 3; ++i) if (date1[i] != date2[i]) return date1[i] < date2[i];  // 연, 월, 일 순서로 비교해 처음 다른 항목에서 date1이 작으면 1, 크면 0을 즉시 반환
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝

// 풀이 요약
// 연도부터 월, 일 순서로 비교. 처음 다른 항목에서 첫 날짜의 값이 더 작아야 이른 날짜이며, 모든 항목이 같으면 0임
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:21:57
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181838_%EB%82%A0%EC%A7%9C_%EB%B9%84%EA%B5%90%ED%95%98%EA%B8%B0/README.md)
