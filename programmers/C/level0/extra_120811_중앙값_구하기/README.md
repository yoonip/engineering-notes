# 중앙값 구하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/120811) · Level 0 · C

## 풀이

복사본을 오름차순 정렬한 뒤 가운데 인덱스 array_len / 2의 원소 반환.

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

static int compare(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}
int solution(int array[], size_t array_len) {
    int* sorted = malloc(array_len * sizeof(*sorted));
    memcpy(sorted, array, array_len * sizeof(*sorted));
    qsort(sorted, array_len, sizeof(*sorted), compare);
    int answer = sorted[array_len / 2];
    free(sorted);
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
// static int compare(const void* a, const void* b) {  // qsort에서 두 정수의 오름차순을 결정할 비교 함수를 정의
//     int x = *(const int*)a, y = *(const int*)b;  // void 포인터를 const int*로 바꾼 뒤 비교할 정수 읽기
//     return (x > y) - (x < y);  // x가 크면 1, 작으면 -1, 같으면 0을 반환해 오름차순 비교 기준 제공
// }  // 블록 끝
// int solution(int array[], size_t array_len) {  // 중앙값 구하기 풀이 시작
//     int* sorted = malloc(array_len * sizeof(*sorted));  // sorted를 저장할 메모리 확보
//     memcpy(sorted, array, array_len * sizeof(*sorted));  // memcpy는 지정한 바이트 수만큼 원본 배열·문자열을 결과 공간으로 복사
//     qsort(sorted, array_len, sizeof(*sorted), compare);  // sorted를 오름차순 정렬
//     int answer = sorted[array_len / 2];  // 정렬된 배열의 가운데 원소가 중앙값
//     free(sorted);  // free는 임시로 확보한 메모리를 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 복사본을 오름차순 정렬한 뒤 가운데 인덱스 array_len / 2의 원소 반환.
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:53:49
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_120811_%EC%A4%91%EC%95%99%EA%B0%92_%EA%B5%AC%ED%95%98%EA%B8%B0/README.md)
