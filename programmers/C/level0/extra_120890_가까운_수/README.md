# 가까운 수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120890) · Level 0 · C

## 풀이

거리 차이를 먼저 비교하고 거리가 같으면 더 작은 원소를 고르기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len, int n) {
    int answer = array[0];
    for (size_t i = 1; i < array_len; ++i)
        if (abs(array[i] - n) < abs(answer - n) || (abs(array[i] - n) == abs(answer - n) && array[i] < answer)) answer = array[i];
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
// int solution(int array[], size_t array_len, int n) {  // 가까운 수 풀이 시작
//     int answer = array[0];  // 첫 원소를 가장 가까운 값의 후보로 선택
//     for (size_t i = 1; i < array_len; ++i)  // 첫 원소 다음부터 n에 더 가까운 후보가 있는지 검사
//         if (abs(array[i] - n) < abs(answer - n) || (abs(array[i] - n) == abs(answer - n) && array[i] < answer)) answer = array[i];  // n과 거리가 더 짧거나, 거리가 같으면서 값이 작을 때 후보 교체
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 거리 차이를 먼저 비교하고 거리가 같으면 더 작은 원소를 고르기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:47:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120890_%EA%B0%80%EA%B9%8C%EC%9A%B4_%EC%88%98/README.md)
