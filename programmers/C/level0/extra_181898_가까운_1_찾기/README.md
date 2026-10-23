# 가까운 1 찾기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181898) · Level 0 · C

## 풀이

시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int arr[], size_t arr_len, int idx) {
    for (size_t i = idx; i < arr_len; ++i) if (arr[i] == 1) return (int)i;
    return -1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int arr[], size_t arr_len, int idx) {  // 가까운 1 찾기 풀이 시작
//     for (size_t i = idx; i < arr_len; ++i) if (arr[i] == 1) return (int)i;  // idx부터 오른쪽으로 검사해 값이 1인 첫 위치 반환
//     return -1;  // 조건을 만족하는 위치가 없으므로 -1을 반환
// }  // 블록 끝
// 풀이 요약
// 시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:10:59
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181898_%EA%B0%80%EA%B9%8C%EC%9A%B4_1_%EC%B0%BE%EA%B8%B0/README.md)
