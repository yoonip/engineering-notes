# 배열 만들기 1

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181901) · Level 0 · C

## 풀이

k부터 n까지 k씩 증가시키며 양의 배수를 저장

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdlib.h>

int* solution(int n, int k) {
    int count = n / k;
    int* answer = malloc((count ? count : 1) * sizeof(int));
    for (int i = 0; i < count; ++i) answer[i] = (i + 1) * k;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
//
// int* solution(int n, int k) {  // 배열 만들기 1 풀이 시작
//     int count = n / k;  // 정수 나눗셈 /로 n 이하인 k의 양의 배수 개수를 구하기
//     int* answer = malloc((count ? count : 1) * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     for (int i = 0; i < count; ++i) answer[i] = (i + 1) * k;  // for로 배수의 개수만큼 순회하며 k의 첫 양의 배수부터 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// k부터 n까지 k씩 증가시키며 양의 배수를 저장
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:10:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181901_%EB%B0%B0%EC%97%B4_%EB%A7%8C%EB%93%A4%EA%B8%B0_1/README.md)
