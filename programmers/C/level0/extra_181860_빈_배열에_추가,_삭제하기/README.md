# 빈 배열에 추가, 삭제하기

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181860) · Level 0 · C

## 풀이

flag가 참이면 지정 개수를 추가하고 거짓이면 끝에서 지정 개수를 삭제

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, bool flag[], size_t flag_len) {
    size_t capacity = 0;
    for (size_t i = 0; i < arr_len; ++i) if (flag[i]) capacity += arr[i] * 2;
    int* work = malloc(capacity * sizeof(int));
    size_t length = 0;
    for (size_t i = 0; i < arr_len; ++i) {
        if (flag[i]) for (int j = 0; j < arr[i] * 2; ++j) work[length++] = arr[i];
        else length -= arr[i];
    }
    int* answer = malloc(length * sizeof(int));
    memcpy(answer, work, length * sizeof(int));
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
// int* solution(int arr[], size_t arr_len, bool flag[], size_t flag_len) {  // 빈 배열에 추가, 삭제하기 풀이 시작
//     size_t capacity = 0;  // 필요한 저장 공간의 크기 저장
//     for (size_t i = 0; i < arr_len; ++i) if (flag[i]) capacity += arr[i] * 2;  // 추가 명령에서 필요한 모든 원소 수를 합산해 임시 배열 최대 용량 계산
//     int* work = malloc(capacity * sizeof(int));  // work를 저장할 메모리 확보
//     size_t length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < arr_len; ++i) {  // 원소와 flag를 짝지어 추가·삭제 명령 적용
//         if (flag[i]) for (int j = 0; j < arr[i] * 2; ++j) work[length++] = arr[i];  // flag가 참이면 현재 값을 그 값의 두 배 횟수만큼 추가
//         else length -= arr[i];  // 삭제 명령이면 끝의 arr[i]개를 논리적 길이에서 제외
//     }  // 블록 끝
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, work, length * sizeof(int));  // 추가·삭제 후 남은 length개 원소만 최종 배열에 복사
//     free(work);  // free로 반환 결과에 사용하지 않는 임시 메모리를 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// flag가 참이면 지정 개수를 추가하고 거짓이면 끝에서 지정 개수를 삭제
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:17:46
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181860_%EB%B9%88_%EB%B0%B0%EC%97%B4%EC%97%90_%EC%B6%94%EA%B0%80%2C_%EC%82%AD%EC%A0%9C%ED%95%98%EA%B8%B0/README.md)
