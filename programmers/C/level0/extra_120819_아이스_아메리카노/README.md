# 아이스 아메리카노

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120819) · Level 0 · C

## 풀이

가격 5500원으로 나눈 몫과 나머지를 사용

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int money) {
    int* answer = malloc(2 * sizeof(*answer));
    answer[0] = money / 5500; answer[1] = money % 5500;
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
// int* solution(int money) {  // 아이스 아메리카노 풀이 시작
//     int* answer = malloc(2 * sizeof(*answer));  // answer를 저장할 메모리 확보
//     answer[0] = money / 5500; answer[1] = money % 5500;  // 살 수 있는 커피 잔 수는 몫, 남은 돈은 나머지
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 가격 5500원으로 나눈 몫과 나머지를 사용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:52:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120819_%EC%95%84%EC%9D%B4%EC%8A%A4_%EC%95%84%EB%A9%94%EB%A6%AC%EC%B9%B4%EB%85%B8/README.md)
