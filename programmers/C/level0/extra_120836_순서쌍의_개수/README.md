# 순서쌍의 개수

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120836) · Level 0 · C

## 풀이

약수 하나가 정해지면 다른 수는 n을 그 약수로 나눈 값임. 같은 두 수인 경우만 한 번 세기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int n) {
    int count = 0;
    for (int i = 1; i <= n / i; ++i)
        if (n % i == 0) count += i == n / i ? 1 : 2;
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
// int solution(int n) {  // 순서쌍의 개수 풀이 시작
//     int count = 0;  // 곱이 n인 순서쌍 개수를 0으로 시작
//     for (int i = 1; i <= n / i; ++i)  // 1부터 n의 제곱근 이하까지 약수 후보 검사
//         if (n % i == 0) count += i == n / i ? 1 : 2;  // 약수 i와 n / i가 다르면 순서를 바꾼 두 쌍, 같으면 한 쌍만 추가
//     return count;  // 모든 약수 쌍으로 센 순서쌍 수 반환
// }  // 블록 끝
// 풀이 요약
// 약수 하나가 정해지면 다른 수는 n을 그 약수로 나눈 값임. 같은 두 수인 경우만 한 번 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:56:18
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120836_%EC%88%9C%EC%84%9C%EC%8C%8D%EC%9D%98_%EA%B0%9C%EC%88%98/README.md)
