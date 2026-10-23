# 머쓱이보다 키 큰 사람

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120585) · Level 0 · C

## 풀이

같은 키는 제외하고 기준 키보다 큰 사람만 세기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len, int height) {
    int count = 0;
    for (size_t i = 0; i < array_len; ++i) count += array[i] > height;
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int array[], size_t array_len, int height) {  // 머쓱이보다 키 큰 사람 풀이 시작
//     int count = 0;  // 기준보다 키가 큰 사람 수를 0으로 시작
//     for (size_t i = 0; i < array_len; ++i) count += array[i] > height;  // 기준 키 height보다 큰 원소마다 참의 값 1을 더함
//     return count;  // 기준보다 키가 큰 사람 수 반환
// }  // 블록 끝
// 풀이 요약
// 같은 키는 제외하고 기준 키보다 큰 사람만 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:55:55
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120585_%EB%A8%B8%EC%93%B1%EC%9D%B4%EB%B3%B4%EB%8B%A4_%ED%82%A4_%ED%81%B0_%EC%82%AC%EB%9E%8C/README.md)
