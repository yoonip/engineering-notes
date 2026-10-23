# 뒤에서 5등 위로

[레벨 0 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/181852) · Level 0 · C

## 풀이

원본의 복사본을 qsort로 오름차순 정렬. 가장 작은 다섯 원소인 인덱스 0~4를 건너뛰고, 인덱스 5부터 끝까지 새 배열에 복사

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
    int* answer = malloc((num_list_len - 5) * sizeof(int));
    memcpy(answer, work + 5, (num_list_len - 5) * sizeof(int));
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
// static int compare_int(const void* a, const void* b) {  // qsort가 두 정수를 비교할 때 호출할 정적 비교 함수를 정의
//     int x = *(const int*)a, y = *(const int*)b;  // void 포인터를 const int 포인터로 변환하고 역참조하여 비교할 정수 x와 y를 읽기
//     return (x > y) - (x < y);  // x가 크면 1, 작으면 -1, 같으면 0을 반환해 오름차순 정렬 기준을 만들기
// }  // 블록 끝
// int* solution(int num_list[], size_t num_list_len) {  // 뒤에서 5등 위로 풀이 시작
//     int* work = malloc(num_list_len * sizeof(int));  // 정렬용 복사본 work에 원래 배열만큼의 int 공간을 할당
//     memcpy(work, num_list, num_list_len * sizeof(int));  // 원본을 바꾸지 않도록 num_list의 원소를 work에 복사
//     qsort(work, num_list_len, sizeof(int), compare_int);  // qsort에 비교 함수 compare_int를 전달하여 work를 오름차순으로 정렬
//     int* answer = malloc((num_list_len - 5) * sizeof(int));  // 다섯 원소를 제외한 num_list_len - 5개의 int를 담을 결과 공간을 할당
//     memcpy(answer, work + 5, (num_list_len - 5) * sizeof(int));  // 포인터 work + 5가 가리키는 여섯 번째 원소부터 마지막까지 answer에 복사
//     free(work);  // 결과 복사가 끝난 임시 정렬 배열 work의 메모리를 해제
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 원본의 복사본을 qsort로 오름차순 정렬. 가장 작은 다섯 원소인 인덱스 0~4를 건너뛰고, 인덱스 5부터 끝까지 새 배열에 복사
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 07:19:05
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level0/extra_181852_%EB%92%A4%EC%97%90%EC%84%9C_5%EB%93%B1_%EC%9C%84%EB%A1%9C/README.md)
