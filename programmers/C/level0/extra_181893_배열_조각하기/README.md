# 배열 조각하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181893) · Level 0 · C

## 풀이

각 쿼리는 이전 작업 후 남은 리스트의 인덱스를 기준으로 적용

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int query[], size_t query_len) {
    int first = 0, last = (int)arr_len - 1;
    for (size_t i = 0; i < query_len; ++i) {
        if (i % 2 == 0) last = first + query[i];
        else first += query[i];
    }
    int* answer = malloc((last - first + 1) * sizeof(int));
    memcpy(answer, arr + first, (last - first + 1) * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int query[], size_t query_len) {  // 배열 조각하기 풀이 시작
//     int first = 0, last = (int)arr_len - 1;  // 남아 있는 원본 구간의 양 끝을 전체 배열 범위로 초기화
//     for (size_t i = 0; i < query_len; ++i) {  // 쿼리를 순서대로 적용하며 남길 구간의 시작·끝 조정
//         if (i % 2 == 0) last = first + query[i];  // 짝수 번째 쿼리는 현재 구간에서 query[i] 뒤쪽을 버리므로 끝 위치 조정
//         else first += query[i];  // 홀수 번째 쿼리는 앞부분을 버리므로 현재 시작점을 query[i]칸 이동
//     }  // 블록 끝
//     int* answer = malloc((last - first + 1) * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, arr + first, (last - first + 1) * sizeof(int));  // 최종적으로 남은 시작점부터 끝점까지 한 번에 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 쿼리는 이전 작업 후 남은 리스트의 인덱스를 기준으로 적용
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:11:28
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181893_%EB%B0%B0%EC%97%B4_%EC%A1%B0%EA%B0%81%ED%95%98%EA%B8%B0/README.md)
