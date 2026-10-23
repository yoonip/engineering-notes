# 짝수 홀수 개수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120824) · Level 0 · C

## 풀이

결과 배열의 0번 칸은 짝수, 1번 칸은 홀수의 개수로 사용. 각 자연수를 2로 나눈 나머지에 해당하는 칸을 하나 증가

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int num_list[], size_t num_list_len) {
    int* answer = calloc(2, sizeof(*answer));
    for (size_t i = 0; i < num_list_len; ++i) ++answer[num_list[i] % 2];
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
// int* solution(int num_list[], size_t num_list_len) {  // 짝수 홀수 개수 풀이 시작
//     int* answer = calloc(2, sizeof(*answer));  // calloc으로 int 두 칸을 할당하면서 0으로 초기화. answer[0]은 짝수 개수, answer[1]은 홀수 개수임
//     for (size_t i = 0; i < num_list_len; ++i) ++answer[num_list[i] % 2];  // 인덱스 i로 입력 배열을 순회하며, 2로 나눈 나머지가 0이면 짝수 칸을, 1이면 홀수 칸을 전위 증가 연산자 ++로 하나 늘림
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 결과 배열의 0번 칸은 짝수, 1번 칸은 홀수의 개수로 사용. 각 자연수를 2로 나눈 나머지에 해당하는 칸을 하나 증가
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:33:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120824_%EC%A7%9D%EC%88%98_%ED%99%80%EC%88%98_%EA%B0%9C%EC%88%98/README.md)
