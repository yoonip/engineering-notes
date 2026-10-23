# 등차수열의 특정한 항만 더하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181931) · Level 0 · C

## 풀이

포함 여부가 참인 인덱스에서 첫 항과 공차로 해당 항을 구해 더하기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdbool.h>
#include <stddef.h>

int solution(int a, int d, bool included[], size_t included_len) {
    int answer = 0;
    for (size_t i = 0; i < included_len; ++i) if (included[i]) answer += a + (int)i * d;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int solution(int a, int d, bool included[], size_t included_len) {  // 등차수열의 특정한 항만 더하기 풀이 시작
//     int answer = 0;  // 정수형 결과 누적값을 0으로 초기화
//     for (size_t i = 0; i < included_len; ++i) if (included[i]) answer += a + (int)i * d;  // for와 if로 포함할 항만 골라 a+i*d를 계산한 뒤 +=로 합계에 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 포함 여부가 참인 인덱스에서 첫 항과 공차로 해당 항을 구해 더하기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:35:42
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181931_%EB%93%B1%EC%B0%A8%EC%88%98%EC%97%B4%EC%9D%98_%ED%8A%B9%EC%A0%95%ED%95%9C_%ED%95%AD%EB%A7%8C_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
