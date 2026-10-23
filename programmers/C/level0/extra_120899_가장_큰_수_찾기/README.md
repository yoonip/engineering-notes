# 가장 큰 수 찾기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120899) · Level 0 · C

## 풀이

최댓값 후보와 그 인덱스를 함께 저장. 더 큰 원소를 찾을 때 두 값을 동시에 갱신하며 배열을 한 번 순회.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int array[], size_t array_len) {
    int* answer = malloc(2 * sizeof(*answer));
    answer[0] = array[0]; answer[1] = 0;
    for (size_t i = 1; i < array_len; ++i)
        if (array[i] > answer[0]) { answer[0] = array[i]; answer[1] = (int)i; }
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
// int* solution(int array[], size_t array_len) {  // 가장 큰 수 찾기 풀이 시작
//     int* answer = malloc(2 * sizeof(*answer));  // answer를 저장할 메모리 확보
//     answer[0] = array[0]; answer[1] = 0;  // 첫 원소를 최댓값 후보로, 그 위치 0을 인덱스 후보로 초기화
//     for (size_t i = 1; i < array_len; ++i)  // 이미 후보로 쓴 첫 원소 다음부터 더 큰 값 탐색
//         if (array[i] > answer[0]) { answer[0] = array[i]; answer[1] = (int)i; }  // 더 큰 값을 만나면 최댓값과 그 인덱스를 함께 교체
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 최댓값 후보와 그 인덱스를 함께 저장. 더 큰 원소를 찾을 때 두 값을 동시에 갱신하며 배열을 한 번 순회.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:40:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120899_%EA%B0%80%EC%9E%A5_%ED%81%B0_%EC%88%98_%EC%B0%BE%EA%B8%B0/README.md)
