# 특별한 이차원 배열 1

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181833) · Level 0 · C

## 풀이

각 행을 calloc으로 0으로 초기화한 뒤 answer[i][i]만 1로 바꾸기. 행 번호와 열 번호가 같은 주대각선만 1인 배열이 됨

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int** solution(int n) {
    int** answer = malloc(n * sizeof(int*));
    for (int i = 0; i < n; ++i) {
        answer[i] = calloc(n, sizeof(int));
        answer[i][i] = 1;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int** solution(int n) {  // 특별한 이차원 배열 1 풀이 시작
//     int** answer = malloc(n * sizeof(int*));  // 행 n개의 시작 주소를 담을 포인터 배열 answer를 할당
//     for (int i = 0; i < n; ++i) {  // 행 번호 i를 0부터 n - 1까지 순회하여 각 행을 만들기
//         answer[i] = calloc(n, sizeof(int));  // 현재 행의 int n개를 calloc으로 할당해 모두 0으로 초기화
//         answer[i][i] = 1;  // 행 번호와 같은 열인 answer[i][i]에 1을 넣어 주대각선을 채움
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 행을 calloc으로 0으로 초기화한 뒤 answer[i][i]만 1로 바꾸기. 행 번호와 열 번호가 같은 주대각선만 1인 배열이 됨
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:22:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181833_%ED%8A%B9%EB%B3%84%ED%95%9C_%EC%9D%B4%EC%B0%A8%EC%9B%90_%EB%B0%B0%EC%97%B4_1/README.md)
