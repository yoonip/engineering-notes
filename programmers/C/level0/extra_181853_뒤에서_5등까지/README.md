# 뒤에서 5등까지

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181853) · Level 0 · C

## 풀이

오름차순 정렬 후 앞 다섯 개를 선택

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

static int compare_int(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}
int* solution(int num_list[], size_t num_list_len) {
    int* work = malloc(num_list_len * sizeof(int));
    memcpy(work, num_list, num_list_len * sizeof(int));
    qsort(work, num_list_len, sizeof(int), compare_int);
    int* answer = malloc(5 * sizeof(int));
    memcpy(answer, work, 5 * sizeof(int));
    free(work);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// static int compare_int(const void* a, const void* b) {  // qsort가 두 정수의 크기를 비교할 때 호출할 보조 함수를 정의
//     int x = *(const int*)a, y = *(const int*)b;  // qsort가 넘긴 두 주소에서 비교할 정수 읽기
//     return (x > y) - (x < y);  // x가 크면 1, 작으면 -1, 같으면 0을 반환해 오름차순 비교 기준 제공
// }  // 블록 끝
// int* solution(int num_list[], size_t num_list_len) {  // 뒤에서 5등까지 풀이 시작
//     int* work = malloc(num_list_len * sizeof(int));  // work를 저장할 메모리 확보
//     memcpy(work, num_list, num_list_len * sizeof(int));  // 원본을 보존하도록 정렬용 복사본 생성
//     qsort(work, num_list_len, sizeof(int), compare_int);  // qsort와 비교 함수를 사용해 원소를 오름차순으로 정렬
//     int* answer = malloc(5 * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, work, 5 * sizeof(int));  // 정렬된 배열의 가장 작은 다섯 원소만 결과에 복사
//     free(work);  // free로 반환 결과에 사용하지 않는 임시 메모리를 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 오름차순 정렬 후 앞 다섯 개를 선택
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 06:18:33
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../Python/level0/extra_181853_%EB%92%A4%EC%97%90%EC%84%9C_5%EB%93%B1%EA%B9%8C%EC%A7%80/README.md)
