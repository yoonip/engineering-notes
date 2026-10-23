# 짝수는 싫어요

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120813) · Level 0 · C

## 풀이

1부터 두 칸 간격으로 증가하면 홀수만 선택됨

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int n) {
    int* answer = malloc(((n + 1) / 2) * sizeof(*answer));
    for (int i = 0; 2 * i + 1 <= n; ++i) answer[i] = 2 * i + 1;
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
// int* solution(int n) {  // 짝수는 싫어요 풀이 시작
//     int* answer = malloc(((n + 1) / 2) * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (int i = 0; 2 * i + 1 <= n; ++i) answer[i] = 2 * i + 1;  // 1, 3, 5, …를 생성해 n 이하인 홀수만 순서대로 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 1부터 두 칸 간격으로 증가하면 홀수만 선택됨
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:31
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120813_%EC%A7%9D%EC%88%98%EB%8A%94_%EC%8B%AB%EC%96%B4%EC%9A%94/README.md)
