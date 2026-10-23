# 369게임

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120891) · Level 0 · C

## 풀이

정수를 10으로 나누며 각 자리 숫자를 확인. 자릿값이 3·6·9 중 하나일 때마다 박수 횟수를 1씩 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int order) {
    int count = 0;
    for (; order; order /= 10) {
        int d = order % 10;
        count += d == 3 || d == 6 || d == 9;
    }
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
// int solution(int order) {  // 369게임 풀이 시작
//     int count = 0;  // int 변수 count를 0으로 초기화하여 3·6·9가 나온 자리 수를 세기
//     for (; order; order /= 10) {  // for는 order에 남은 자리가 있는 동안 반복하며, 반복 끝의 order /= 10으로 방금 검사한 일의 자리를 제거
//         int d = order % 10;  // 나머지 연산 order % 10으로 현재 일의 자리 숫자를 d에 저장
//         count += d == 3 || d == 6 || d == 9;  // 논리 OR 연산자 ||로 d가 3·6·9 중 하나인지 검사. 참이면 1, 거짓이면 0을 count에 더하기
//     }  // 블록 끝
//     return count;  // return으로 전체 자리에서 센 박수 횟수 count를 반환
// }  // 블록 끝

// 풀이 요약
// 정수를 10으로 나누며 각 자리 숫자를 확인. 자릿값이 3·6·9 중 하나일 때마다 박수 횟수를 1씩 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:27:56
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120891_369%EA%B2%8C%EC%9E%84/README.md)
