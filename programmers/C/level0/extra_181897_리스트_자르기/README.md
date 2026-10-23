# 리스트 자르기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181897) · Level 0 · C

## 풀이

n에 따라 슬라이싱의 시작·끝·간격을 선택

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int n, int slicer[], size_t slicer_len, int num_list[], size_t num_list_len) {
    int begin = n == 1 ? 0 : slicer[0];
    int end = n == 2 ? (int)num_list_len - 1 : slicer[1];
    int step = n == 4 ? slicer[2] : 1;
    int length = (end - begin) / step + 1;
    int* answer = malloc(length * sizeof(int));
    for (int i = 0; i < length; ++i) answer[i] = num_list[begin + i * step];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int n, int slicer[], size_t slicer_len, int num_list[], size_t num_list_len) {  // 리스트 자르기 풀이 시작
//     int begin = n == 1 ? 0 : slicer[0];  // 포함할 구간의 시작 위치 저장
//     int end = n == 2 ? (int)num_list_len - 1 : slicer[1];  // 구간의 끝 위치 저장
//     int step = n == 4 ? slicer[2] : 1;  // 4번 방식만 slicer의 간격을 사용하고, 나머지는 한 칸씩 이동
//     int length = (end - begin) / step + 1;  // 결과의 원소 수 저장
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     for (int i = 0; i < length; ++i) answer[i] = num_list[begin + i * step];  // 선택한 시작점에서 step 간격으로 원소를 읽어 결과에 순서대로 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// n에 따라 슬라이싱의 시작·끝·간격을 선택
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:03:36
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181897_%EB%A6%AC%EC%8A%A4%ED%8A%B8_%EC%9E%90%EB%A5%B4%EA%B8%B0/README.md)
