# 최빈값 구하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120812) · Level 0 · C

## 풀이

등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len) {
    int counts[1000] = {0}, answer = -1, best = 0;
    for (size_t i = 0; i < array_len; ++i) ++counts[array[i]];
    for (int i = 0; i < 1000; ++i) {
        if (counts[i] > best) { best = counts[i]; answer = i; }
        else if (counts[i] == best) answer = -1;
    }
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
// int solution(int array[], size_t array_len) {  // 최빈값 구하기 풀이 시작
//     int counts[1000] = {0}, answer = -1, best = 0;  // 값별 빈도 배열, 최빈값 후보 answer, 최대 빈도 best 준비
//     for (size_t i = 0; i < array_len; ++i) ++counts[array[i]];  // 숫자마다 나온 횟수를 counts에 누적
//     for (int i = 0; i < 1000; ++i) {  // 가능한 값 0부터 999까지의 빈도 비교
//         if (counts[i] > best) { best = counts[i]; answer = i; }  // 더 많이 나온 숫자를 찾으면 최빈값 후보 교체
//         else if (counts[i] == best) answer = -1;  // 같은 최대 빈도를 가진 다른 값이 있으면 최빈값이 여러 개라는 -1 표시
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120812_%EC%B5%9C%EB%B9%88%EA%B0%92_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
