# 달리기 경주

[레벨 1 목록](../README.md) · [C 전체 목록](../../README.md) · [프로그래머스](../../../README.md)

[공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/178871) · Level 1 · C

## 풀이

선수 이름별 현재 위치를 해시 테이블에 저장; 호명된 선수와 바로 앞 선수를 교환하고 두 위치를 함께 갱신

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

static char* copy_text(const char* text) {
    char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;
}
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
char** solution(const char* players[], size_t players_len, const char* callings[], size_t callings_len) {
    size_t capacity = 1; while (capacity < players_len * 2) capacity *= 2;
    MapEntry* position = calloc(capacity, sizeof(MapEntry));
    char** answer = malloc(players_len * sizeof(char*));
    for (size_t i = 0; i < players_len; ++i) {
        answer[i] = copy_text(players[i]); size_t slot = map_slot(position, capacity, players[i]); position[slot].key = players[i]; position[slot].value = (int)i;
    }
    for (size_t q = 0; q < callings_len; ++q) {
        size_t slot = map_slot(position, capacity, callings[q]); int i = position[slot].value;
        char* front = answer[i - 1]; answer[i - 1] = answer[i]; answer[i] = front;
        position[slot].value = i - 1; position[map_slot(position, capacity, front)].value = i;
    }
    free(position);
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
// static char* copy_text(const char* text) {  // 문자열을 새 공간에 복사해서 돌려주기
//     char* result = malloc(strlen(text) + 1); strcpy(result, text); return result;  // 선수 이름 문자열 사본 공간 확보
// }  // 이 범위 끝
// typedef struct { const char* key; int value; } MapEntry;  // 선수 이름과 현재 등수를 한 해시 항목으로 묶기
// static size_t hash_word(const char* key) {  // 문자열 바이트를 섞어 이름 해시 만들기
//     size_t hash = 2166136261u;  // 문자열 해시를 시작할 FNV 초기값
//     for (; *key; ++key) hash = (hash ^ (unsigned char)*key) * 16777619u;  // 각 바이트를 XOR로 섞고 소수를 곱해 문자열 해시를 누적하기
//     return hash;  // 문자열을 모두 섞은 해시 값 반환
// }  // 이 범위 끝
// static size_t map_slot(MapEntry* map, size_t capacity, const char* key) {  // 같은 이름 또는 빈 해시 칸까지 선형 탐색
//     size_t slot = hash_word(key) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     while (map[slot].key && strcmp(map[slot].key, key)) slot = (slot + 1) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     return slot;  // 선수 이름의 해시 칸 반환
// }  // 이 범위 끝
// char** solution(const char* players[], size_t players_len, const char* callings[], size_t callings_len) {  // 선수 이름별 현재 위치를 해시 테이블에 저장; 호명된 선수와 바로 앞 선수를 교환하고 두 위치를 함께 갱신
//     size_t capacity = 1; while (capacity < players_len * 2) capacity *= 2;  // 선수 수 두 배 이상의 2의 거듭제곱으로 해시표 크기 설정
//     MapEntry* position = calloc(capacity, sizeof(MapEntry));  // 선수 이름별 현재 순위 공간 확보하고 0으로 시작
//     char** answer = malloc(players_len * sizeof(char*));  // 현재 순서로 놓은 선수 이름 공간 확보
//     for (size_t i = 0; i < players_len; ++i) {  // 호명된 선수의 현재 위치 순서대로 확인
//         answer[i] = copy_text(players[i]); size_t slot = map_slot(position, capacity, players[i]); position[slot].key = players[i]; position[slot].value = (int)i;  // 현재 순서로 놓은 선수 이름 / 선수 이름의 해시 칸 갱신
//     }  // 이 범위 끝
//     for (size_t q = 0; q < callings_len; ++q) {  // 처리할 호명 위치 순서대로 확인
//         size_t slot = map_slot(position, capacity, callings[q]); int i = position[slot].value;  // 선수 이름의 해시 칸 / 호명된 선수의 현재 위치 저장
//         char* front = answer[i - 1]; answer[i - 1] = answer[i]; answer[i] = front;  // 바로 앞 선수 이름 / 현재 순서로 놓은 선수 이름 저장
//         position[slot].value = i - 1; position[map_slot(position, capacity, front)].value = i;  // 선수 이름별 현재 순위 / 선수 이름의 해시 칸 / 호명된 선수의 현재 위치 / 해시표 칸 수 확인
//     }  // 이 범위 끝
//     free(position);  // 선수 이름별 현재 순위 임시 공간 정리
//     return answer;  // 현재 순서로 놓은 선수 이름 반환
// }  // 이 범위 끝

// 풀이 요약
// 선수 이름별 현재 위치를 해시 테이블에 저장; 호명된 선수와 바로 앞 선수를 교환하고 두 위치를 함께 갱신
```

## 채점 기록

- 언어: C
- 결과: 정답 100/100
- 제출 기록: 2026-10-24 05:45:58
- 확인 날짜: 2026-10-24

[기존 풀이 기록](../../../level1/extra_178871_%EB%8B%AC%EB%A6%AC%EA%B8%B0_%EA%B2%BD%EC%A3%BC/README.md)
