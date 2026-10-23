# 신고 결과 받기

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/92334) · Level 1 · C

## 풀이

신고자와 대상의 쌍을 중복 없이 기록; 대상의 신고 횟수가 k 이상이면 해당 신고자에게 보낼 메일 수를 늘리기

## 코드와 줄별 설명

[코드 파일](solution.c) · [채점 기록](grading.json)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

typedef struct { const char* key; int value; } MapEntry;
static size_t hash_word(const char* key) {
    size_t hash = 2166136261u;
    for (; *key; ++key) hash = (hash ^ (unsigned char)*key) * 16777619u;
    return hash;
}
static size_t map_slot(MapEntry* map, size_t capacity, const char* key) {
    size_t slot = hash_word(key) & (capacity - 1);
    while (map[slot].key && strcmp(map[slot].key, key)) slot = (slot + 1) & (capacity - 1);
    return slot;
}
int* solution(const char* id_list[], size_t id_list_len, const char* report[], size_t report_len, int k) {
    size_t n = id_list_len, capacity = 1; while (capacity < n * 2) capacity *= 2;
    MapEntry* index = calloc(capacity, sizeof(MapEntry));
    for (size_t i = 0; i < n; ++i) { size_t slot = map_slot(index, capacity, id_list[i]); index[slot].key = id_list[i]; index[slot].value = (int)i; }
    bool* reported = calloc(n * n, sizeof(bool)); int* counts = calloc(n, sizeof(int));
    for (size_t i = 0; i < report_len; ++i) {
        char a[11], b[11]; sscanf(report[i], "%10s %10s", a, b);
        int reporter = index[map_slot(index, capacity, a)].value, target = index[map_slot(index, capacity, b)].value;
        if (!reported[reporter * n + target]) { reported[reporter * n + target] = true; ++counts[target]; }
    }
    int* answer = calloc(n, sizeof(int));
    for (size_t i = 0; i < n; ++i) for (size_t j = 0; j < n; ++j) if (reported[i * n + j] && counts[j] >= k) ++answer[i];
    free(index); free(reported); free(counts);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// typedef struct { const char* key; int value; } MapEntry;  // 사용자 이름과 사용자 번호를 한 해시 항목으로 묶기
// static size_t hash_word(const char* key) {  // 문자열 바이트를 섞어 이름 해시 만들기
//     size_t hash = 2166136261u;  // 문자열 해시를 시작할 FNV 초기값
//     for (; *key; ++key) hash = (hash ^ (unsigned char)*key) * 16777619u;  // 각 바이트를 XOR로 섞고 소수를 곱해 문자열 해시를 누적하기
//     return hash;  // 문자열을 모두 섞은 해시 값 반환
// }  // 이 범위 끝
// static size_t map_slot(MapEntry* map, size_t capacity, const char* key) {  // 같은 이름 또는 빈 해시 칸까지 선형 탐색
//     size_t slot = hash_word(key) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     while (map[slot].key && strcmp(map[slot].key, key)) slot = (slot + 1) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     return slot;  // 아이디가 들어갈 해시 칸 반환
// }  // 이 범위 끝
// int* solution(const char* id_list[], size_t id_list_len, const char* report[], size_t report_len, int k) {  // 신고자와 대상의 쌍을 중복 없이 기록; 대상의 신고 횟수가 k 이상이면 해당 신고자에게 보낼 메일 수를 늘리기
//     size_t n = id_list_len, capacity = 1; while (capacity < n * 2) capacity *= 2;  // 전체 사용자 수 / 해시표 칸 수 저장
//     MapEntry* index = calloc(capacity, sizeof(MapEntry));  // 아이디를 사용자 번호로 바꾸는 해시표 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < n; ++i) { size_t slot = map_slot(index, capacity, id_list[i]); index[slot].key = id_list[i]; index[slot].value = (int)i; }  // 신고자 또는 입력 기록 위치 순서대로 확인; 아이디가 들어갈 해시 칸 저장
//     bool* reported = calloc(n * n, sizeof(bool)); int* counts = calloc(n, sizeof(int));  // 신고자와 대상의 중복 신고 표시 / 대상별 서로 다른 신고자 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < report_len; ++i) {  // 신고자 또는 입력 기록 위치 순서대로 확인
//         char a[11], b[11]; sscanf(report[i], "%10s %10s", a, b);  // 신고한 사용자와 신고당한 사용자 이름 읽기
//         int reporter = index[map_slot(index, capacity, a)].value, target = index[map_slot(index, capacity, b)].value;  // 신고한 사용자 번호 / 신고받은 사용자 번호 저장
//         if (!reported[reporter * n + target]) { reported[reporter * n + target] = true; ++counts[target]; }  // 같은 신고자가 같은 대상을 처음 신고했을 때만 대상 신고 수 늘리기
//     }  // 이 범위 끝
//     int* answer = calloc(n, sizeof(int));  // 사용자별 받을 메일 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < n; ++i) for (size_t j = 0; j < n; ++j) if (reported[i * n + j] && counts[j] >= k) ++answer[i];  // 신고자 또는 입력 기록 위치 순서대로 확인; 신고 대상 사용자 번호 / 사용자별 받을 메일 수 갱신
//     free(index); free(reported); free(counts);  // 아이디를 사용자 번호로 바꾸는 해시표 / 신고자와 대상의 중복 신고 표시 / 대상별 서로 다른 신고자 수 임시 공간 정리
//     return answer;  // 사용자별 받을 메일 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 신고자와 대상의 쌍을 중복 없이 기록; 대상의 신고 횟수가 k 이상이면 해당 신고자에게 보낼 메일 수를 늘리기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:52:22
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_92334_%EC%8B%A0%EA%B3%A0_%EA%B2%B0%EA%B3%BC_%EB%B0%9B%EA%B8%B0/README.md)
