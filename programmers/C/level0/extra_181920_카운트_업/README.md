# 카운트 업

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181920) · Level 0 · C

## 풀이

시작값부터 끝값까지 1씩 증가하는 정수를 저장

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>

int* solution(int start_num, int end_num) {
    int count = end_num - start_num + 1;
    int* answer = malloc(count * sizeof(int));
    for (int i = 0; i < count; ++i) answer[i] = start_num + i;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
//
// int* solution(int start_num, int end_num) {  // 카운트 업 풀이 시작
//     int count = end_num - start_num + 1;  // 양 끝을 포함한 정수 개수를 뺄셈과 덧셈으로 구하기
//     int* answer = malloc(count * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     for (int i = 0; i < count; ++i) answer[i] = start_num + i;  // for로 결과 인덱스를 순회하며 시작값에 인덱스를 더한 수를 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 시작값부터 끝값까지 1씩 증가하는 정수를 저장
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:44:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181920_%EC%B9%B4%EC%9A%B4%ED%8A%B8_%EC%97%85/README.md)
