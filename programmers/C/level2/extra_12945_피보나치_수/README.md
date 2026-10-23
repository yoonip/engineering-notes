# 피보나치 수

[레벨 2 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12945) · Level 2 · C

## 풀이

다음 수는 직전 두 수의 합이므로 두 변수로 순서대로 갱신하기; 매번 나머지를 취해 수가 지나치게 커지는 것을 막는다
예: (0,1)→(1,1)→(1,2)→(2,3)이므로 n=3의 답은 2.; 시간 O(N), 공간 O(1)

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int n) {
    int previous = 0, current = 1;
    for (int i = 0; i < n; ++i) {
        int next = (previous + current) % 1234567;
        previous = current; current = next;
    }
    return previous;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// int solution(int n) {  // 다음 수는 직전 두 수의 합이므로 두 변수로 순서대로 갱신하기; 매번 나머지를 취해 수가 지나치게 커지는 것을 막는다
//     int previous = 0, current = 1;  // 이전 피보나치 수 / 현재 피보나치 수 저장
//     for (int i = 0; i < n; ++i) {  // 피보나치 수를 옮긴 횟수 순서대로 확인
//         int next = (previous + current) % 1234567;  // 다음 피보나치 수 저장
//         previous = current; current = next;  // 이전 피보나치 수 / 현재 피보나치 수 갱신
//     }  // 이 범위 끝
//     return previous;  // 이전 피보나치 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 다음 수는 직전 두 수의 합이므로 두 변수로 순서대로 갱신하기; 매번 나머지를 취해 수가 지나치게 커지는 것을 막는다
// 예: (0,1)→(1,1)→(1,2)→(2,3)이므로 n=3의 답은 2.; 시간 O(N), 공간 O(1)
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:22:32
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level2/extra_12945_%ED%94%BC%EB%B3%B4%EB%82%98%EC%B9%98_%EC%88%98/README.md)
