# flag에 따라 다른 값 반환하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181933) · Level 0 · C

## 풀이

flag가 참이면 두 정수를 더하고, 거짓이면 빼기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdbool.h>

int solution(int a, int b, bool flag) {
    return flag ? a + b : a - b;
}

// 전체 코드 줄별 설명
// #include <stdbool.h>  // C에서 bool·true·false 사용
//
// int solution(int a, int b, bool flag) {  // flag에 따라 다른 값 반환하기 풀이 시작
//     return flag ? a + b : a - b;  // 삼항 연산자 ?:로 flag에 따라 합 또는 차를 반환
// }  // 블록 끝

// 풀이 요약
// flag가 참이면 두 정수를 더하고, 거짓이면 빼기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:30:50
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181933_flag%EC%97%90_%EB%94%B0%EB%9D%BC_%EB%8B%A4%EB%A5%B8_%EA%B0%92_%EB%B0%98%ED%99%98%ED%95%98%EA%B8%B0/README.md)
