# A로 B 만들기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120886) · Level 0 · C

## 풀이

before의 문자 빈도는 더하고 after의 빈도는 뺌. 모든 알파벳의 차이가 0이면 순서만 바꾸어 같은 문자열을 만들 수 있음.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* before, const char* after) {
    int counts[26] = {0};
    for (size_t i = 0; before[i]; ++i) ++counts[before[i] - 'a'];
    for (size_t i = 0; after[i]; ++i) --counts[after[i] - 'a'];
    for (int i = 0; i < 26; ++i) if (counts[i]) return 0;
    return 1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* before, const char* after) {  // A로 B 만들기 풀이 시작
//     int counts[26] = {0};  // 두 문자열 사이 소문자별 빈도 차이를 저장할 26칸 배열 준비
//     for (size_t i = 0; before[i]; ++i) ++counts[before[i] - 'a'];  // before 문자의 빈도는 더하기
//     for (size_t i = 0; after[i]; ++i) --counts[after[i] - 'a'];  // after 문자의 빈도는 빼기. 모두 0이면 두 문자열의 문자 구성이 같음
//     for (int i = 0; i < 26; ++i) if (counts[i]) return 0;  // 한 문자라도 빈도 차이가 남으면 재배열로 만들 수 없어 0 반환
//     return 1;  // return으로 조건을 만족한다는 지정 값 1을 반환
// }  // 블록 끝
// 풀이 요약
// before의 문자 빈도는 더하고 after의 빈도는 뺌. 모든 알파벳의 차이가 0이면 순서만 바꾸어 같은 문자열을 만들 수 있음.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:48:37
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120886_A%EB%A1%9C_B_%EB%A7%8C%EB%93%A4%EA%B8%B0/README.md)
