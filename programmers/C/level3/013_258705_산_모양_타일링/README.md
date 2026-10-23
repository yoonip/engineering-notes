# 산 모양 타일링

[레벨 3 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258705) · Level 3 · C

## 풀이

오른쪽 끝의 삼각형이 이전 삼각형과 묶였는지로 상태를 두 개만 유지하는 DP
새 오른쪽을 마름모로 묶는 방법은 이전 전체 경우의 수; 새 오른쪽이 단독이면 왼쪽 끝의 사용 여부와 top에 따라 1+top 또는 2+top가지로 확장하기; 시간 O(N), 추가 공간 O(1)
예: tops=[0,1]이면 (joined,free)는 (0,1)→(1,2)→(3,8).; 총 11가지

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int n, int tops[], size_t tops_len) {
    (void)n; int joined = 0, free_tiles = 1;
    for (size_t i = 0; i < tops_len; ++i) { int next_joined = (joined + free_tiles) % 10007, next_free = ((1 + tops[i]) * joined + (2 + tops[i]) * free_tiles) % 10007; joined = next_joined; free_tiles = next_free; }
    return (joined + free_tiles) % 10007;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int n, int tops[], size_t tops_len) {  // 오른쪽 끝의 삼각형이 이전 삼각형과 묶였는지로 상태를 두 개만 유지하는 DP
//     (void)n; int joined = 0, free_tiles = 1;  // 오른쪽 경계와 이어진 타일 배치 수 / 오른쪽 경계가 자유로운 배치 수 갱신
//     for (size_t i = 0; i < tops_len; ++i) { int next_joined = (joined + free_tiles) % 10007, next_free = ((1 + tops[i]) * joined + (2 + tops[i]) * free_tiles) % 10007; joined = next_joined; free_tiles = next_free; }  // 위 삼각형을 확인할 위치 순서대로 확인; 다음 삼각형 뒤 연결 상태 수 / 다음 삼각형 뒤 자유 상태 수 / 오른쪽 경계와 이어진 타일 배치 수 / 오른쪽 경계가 자유로운 배치 수 저장
//     return (joined + free_tiles) % 10007;  // 오른쪽 경계와 이어진 타일 배치 수 / 오른쪽 경계가 자유로운 배치 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 오른쪽 끝의 삼각형이 이전 삼각형과 묶였는지로 상태를 두 개만 유지하는 DP
// 새 오른쪽을 마름모로 묶는 방법은 이전 전체 경우의 수; 새 오른쪽이 단독이면 왼쪽 끝의 사용 여부와 top에 따라 1+top 또는 2+top가지로 확장하기; 시간 O(N), 추가 공간 O(1)
// 예: tops=[0,1]이면 (joined,free)는 (0,1)→(1,2)→(3,8).; 총 11가지
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:27:42
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level3/013_258705_%EC%82%B0_%EB%AA%A8%EC%96%91_%ED%83%80%EC%9D%BC%EB%A7%81/README.md)
