# 문자열 정렬하기 (1)

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120850) · Level 0 · C

## 풀이

문자열에서 한 자리 숫자를 골라 정수로 바꾼 뒤 정렬

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(const char* my_string) {
    int counts[10] = {0};
    size_t len = strlen(my_string), pos = 0;
    int* answer = malloc((len ? len : 1) * sizeof(*answer));
    for (size_t i = 0; i < len; ++i)
        if (isdigit((unsigned char)my_string[i])) ++counts[my_string[i] - '0'];
    for (int d = 0; d < 10; ++d)
        for (int j = 0; j < counts[d]; ++j) answer[pos++] = d;
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
// int* solution(const char* my_string) {  // 문자열 정렬하기 (1) 풀이 시작
//     int counts[10] = {0};  // 숫자 0부터 9까지의 등장 횟수를 0으로 초기화
//     size_t len = strlen(my_string), pos = 0;  // len에 입력 문자열 길이 저장 · 다음 문자를 쓸 위치는 0부터 시작
//     int* answer = malloc((len ? len : 1) * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < len; ++i)  // 문자열에서 숫자 문자의 등장 횟수 기록
//         if (isdigit((unsigned char)my_string[i])) ++counts[my_string[i] - '0'];  // 숫자 문자에 해당하는 빈도 칸을 1 증가
//     for (int d = 0; d < 10; ++d)  // 결과를 오름차순으로 만들도록 숫자 0부터 9까지 처리
//         for (int j = 0; j < counts[d]; ++j) answer[pos++] = d;  // 숫자 d가 나온 횟수만큼 결과에 넣기. 작은 숫자부터 처리
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 문자열에서 한 자리 숫자를 골라 정수로 바꾼 뒤 정렬
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:57:40
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_120850_%EB%AC%B8%EC%9E%90%EC%97%B4_%EC%A0%95%EB%A0%AC%ED%95%98%EA%B8%B0_%281%29/README.md)
