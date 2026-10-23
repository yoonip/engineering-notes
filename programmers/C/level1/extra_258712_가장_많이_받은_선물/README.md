# 가장 많이 받은 선물

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/258712) · Level 1 · C

## 풀이

친구별 선물 전달 횟수와 준 개수에서 받은 개수를 뺀 선물 지수를 기록; 두 친구의 기록을 비교해 다음 달 받을 선물 수를 세기

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
int solution(const char* friends[], size_t friends_len, const char* gifts[], size_t gifts_len) {
    size_t n = friends_len, capacity = 1;
    while (capacity < n * 2) capacity *= 2;
    MapEntry* map = calloc(capacity, sizeof(MapEntry));
    for (size_t i = 0; i < n; ++i) { size_t slot = map_slot(map, capacity, friends[i]); map[slot].key = friends[i]; map[slot].value = (int)i; }
    int* given = calloc(n * n, sizeof(int)); int* score = calloc(n, sizeof(int)); int* received = calloc(n, sizeof(int));
    for (size_t i = 0; i < gifts_len; ++i) {
        char a[11], b[11]; sscanf(gifts[i], "%10s %10s", a, b);
        int giver = map[map_slot(map, capacity, a)].value, receiver = map[map_slot(map, capacity, b)].value;
        ++given[giver * n + receiver]; ++score[giver]; --score[receiver];
    }
    for (size_t i = 0; i < n; ++i) for (size_t j = i + 1; j < n; ++j) {
        int a = given[i * n + j], b = given[j * n + i];
        if (a > b || (a == b && score[i] > score[j])) ++received[i];
        else if (a < b || (a == b && score[i] < score[j])) ++received[j];
    }
    int answer = 0; for (size_t i = 0; i < n; ++i) if (received[i] > answer) answer = received[i];
    free(map); free(given); free(score); free(received);
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
// typedef struct { const char* key; int value; } MapEntry;  // 친구 이름과 친구 번호를 한 해시 항목으로 묶기
// static size_t hash_word(const char* key) {  // 문자열 바이트를 섞어 이름 해시 만들기
//     size_t hash = 2166136261u;  // 문자열 해시를 시작할 FNV 초기값
//     for (; *key; ++key) hash = (hash ^ (unsigned char)*key) * 16777619u;  // 각 바이트를 XOR로 섞고 소수를 곱해 문자열 해시를 누적하기
//     return hash;  // 문자열을 모두 섞은 해시 값 반환
// }  // 이 범위 끝
// static size_t map_slot(MapEntry* map, size_t capacity, const char* key) {  // 같은 이름 또는 빈 해시 칸까지 선형 탐색
//     size_t slot = hash_word(key) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     while (map[slot].key && strcmp(map[slot].key, key)) slot = (slot + 1) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     return slot;  // 친구 이름을 찾은 해시 칸 번호 반환
// }  // 이 범위 끝
// int solution(const char* friends[], size_t friends_len, const char* gifts[], size_t gifts_len) {  // 친구별 선물 전달 횟수와 준 개수에서 받은 개수를 뺀 선물 지수를 기록; 두 친구의 기록을 비교해 다음 달 받을 선물 수를 세기
//     size_t n = friends_len, capacity = 1;  // 친구 수 / 해시표 칸 수 저장
//     while (capacity < n * 2) capacity *= 2;  // 친구 수의 두 배 이상이 되는 2의 거듭제곱으로 해시표 크기 잡기
//     MapEntry* map = calloc(capacity, sizeof(MapEntry));  // 이름을 친구 번호로 바꾸는 해시표 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < n; ++i) { size_t slot = map_slot(map, capacity, friends[i]); map[slot].key = friends[i]; map[slot].value = (int)i; }  // 첫 친구 또는 선물 기록 위치 순서대로 확인; 이름을 친구 번호로 바꾸는 해시표 / 해시표 칸 수 / 첫 친구 또는 선물 기록 위치 확인
//     int* given = calloc(n * n, sizeof(int)); int* score = calloc(n, sizeof(int)); int* received = calloc(n, sizeof(int));  // 친구 쌍별 주고받은 선물 수 / 준 수에서 받은 수를 뺀 선물 지수 / 다음 달 받을 선물 수 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < gifts_len; ++i) {  // 첫 친구 또는 선물 기록 위치 순서대로 확인
//         char a[11], b[11]; sscanf(gifts[i], "%10s %10s", a, b);  // 선물을 준 친구와 받은 친구 이름 읽기
//         int giver = map[map_slot(map, capacity, a)].value, receiver = map[map_slot(map, capacity, b)].value;  // 준 친구 번호 / 받은 친구 번호 저장
//         ++given[giver * n + receiver]; ++score[giver]; --score[receiver];  // 친구 쌍별 주고받은 선물 수 / 준 수에서 받은 수를 뺀 선물 지수 갱신
//     }  // 이 범위 끝
//     for (size_t i = 0; i < n; ++i) for (size_t j = i + 1; j < n; ++j) {  // 첫 친구 또는 선물 기록 위치 순서대로 확인; 둘째 친구 번호 갱신
//         int a = given[i * n + j], b = given[j * n + i];  // 한 방향으로 준 선물 수 / 반대 방향으로 준 선물 수 저장
//         if (a > b || (a == b && score[i] > score[j])) ++received[i];  // i가 j에게 더 많이 줬거나 동률에서 선물 지수가 높으면 i가 받을 선물 추가
//         else if (a < b || (a == b && score[i] < score[j])) ++received[j];  // j가 i에게 더 많이 줬거나 동률에서 선물 지수가 높으면 j가 받을 선물 추가
//     }  // 이 범위 끝
//     int answer = 0; for (size_t i = 0; i < n; ++i) if (received[i] > answer) answer = received[i];  // 다음 달 가장 많이 받을 개수 / 첫 친구 또는 선물 기록 위치 저장
//     free(map); free(given); free(score); free(received);  // 이름을 친구 번호로 바꾸는 해시표 / 친구 쌍별 주고받은 선물 수 / 준 수에서 받은 수를 뺀 선물 지수 / 다음 달 받을 선물 수 임시 공간 정리
//     return answer;  // 다음 달 가장 많이 받을 개수 반환
// }  // 이 범위 끝

// 풀이 요약
// 친구별 선물 전달 횟수와 준 개수에서 받은 개수를 뺀 선물 지수를 기록; 두 친구의 기록을 비교해 다음 달 받을 선물 수를 세기
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:45:26
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_258712_%EA%B0%80%EC%9E%A5_%EB%A7%8E%EC%9D%B4_%EB%B0%9B%EC%9D%80_%EC%84%A0%EB%AC%BC/README.md)
