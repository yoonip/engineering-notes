# n보다 커질 때까지 더하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181884) · Level 0 · C

## 풀이

앞에서부터 더하며 누적합이 처음 n을 초과하는 순간 종료. n과 같을 때는 다음 원소도 더함.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int numbers[], size_t numbers_len, int n) {
    int sum = 0;
    for (size_t i = 0; i < numbers_len && sum <= n; ++i) sum += numbers[i];
    return sum;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int numbers[], size_t numbers_len, int n) {  // n보다 커질 때까지 더하기 풀이 시작
//     int sum = 0;  // 누적 합계 저장
//     for (size_t i = 0; i < numbers_len && sum <= n; ++i) sum += numbers[i];  // 누적합이 n 이하인 동안 다음 수를 더해, 처음 n을 초과하면 종료
//     return sum;  // 처음으로 n을 초과하게 된 누적합 반환
// }  // 블록 끝// 풀이 요약
// 앞에서부터 더하며 누적합이 처음 n을 초과하는 순간 종료. n과 같을 때는 다음 원소도 더함.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:13:23
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181884_n%EB%B3%B4%EB%8B%A4_%EC%BB%A4%EC%A7%88_%EB%95%8C%EA%B9%8C%EC%A7%80_%EB%8D%94%ED%95%98%EA%B8%B0/README.md)
