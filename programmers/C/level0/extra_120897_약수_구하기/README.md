# 약수 구하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120897) · Level 0 · C

## 풀이

1부터 n까지 오름차순으로 검사하여 n을 나누어떨어지게 하는 값만 저장. 작은 후보부터 확인하므로 결과도 오름차순임

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int n) {
    int* answer = malloc(n * sizeof(*answer));
    int pos = 0;
    for (int d = 1; d <= n; ++d) if (n % d == 0) answer[pos++] = d;
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
// int* solution(int n) {  // 약수 구하기 풀이 시작
//     int* answer = malloc(n * sizeof(*answer));  // 약수의 개수는 n을 넘지 않으므로 정수 n개를 담을 결과 공간을 malloc으로 확보
//     int pos = 0;  // int 변수 pos는 찾은 약수의 개수이자 다음 약수를 기록할 위치이며, 0에서 시작
//     for (int d = 1; d <= n; ++d) if (n % d == 0) answer[pos++] = d;  // for로 후보 d를 1부터 n까지 오름차순으로 검사. n % d가 0일 때만 d를 결과에 넣고 pos를 증가
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 1부터 n까지 오름차순으로 검사하여 n을 나누어떨어지게 하는 값만 저장. 작은 후보부터 확인하므로 결과도 오름차순임
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:26:53
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120897_%EC%95%BD%EC%88%98_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
