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
int solution(const char* message, int** spoiler_ranges, size_t spoiler_ranges_rows, size_t spoiler_ranges_cols) {
    size_t n = strlen(message), capacity = 1;
    size_t words = 1; for (size_t i = 0; i < n; ++i) if (message[i] == ' ') ++words;
    while (capacity < 2 * words) capacity *= 2;
    MapEntry* map = calloc(capacity, sizeof(MapEntry));
    int* difference = calloc(n + 1, sizeof(int));
    for (size_t r = 0; r < spoiler_ranges_rows; ++r) { ++difference[spoiler_ranges[r][0]]; --difference[spoiler_ranges[r][1] + 1]; }
    int cover = 0; size_t start = 0; bool hidden = false;
    for (size_t i = 0; i <= n; ++i) {
        if (i < n) cover += difference[i];
        if (i == n || message[i] == ' ') {
            if (i > start) {
                char* word = malloc(i - start + 1); memcpy(word, message + start, i - start); word[i - start] = '\0';
                size_t slot = map_slot(map, capacity, word);
                if (!map[slot].key) map[slot].key = word; else free(word);
                map[slot].value |= hidden ? 2 : 1;
            }
            start = i + 1; hidden = false;
        } else if (cover > 0) hidden = true;
    }
    int answer = 0;
    for (size_t i = 0; i < capacity; ++i) if (map[i].key) { if (map[i].value == 2) ++answer; free((void*)map[i].key); }
    free(map); free(difference);
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
// typedef struct { const char* key; int value; } MapEntry;  // 단어 문자열과 공개·가림 여부 비트를 한 해시 항목으로 묶기
// static size_t hash_word(const char* key) {  // 문자열 바이트를 섞어 이름 해시 만들기
//     size_t hash = 2166136261u;  // 문자열 해시를 시작할 FNV 초기값
//     for (; *key; ++key) hash = (hash ^ (unsigned char)*key) * 16777619u;  // 각 바이트를 XOR로 섞고 소수를 곱해 문자열 해시를 누적하기
//     return hash;  // 문자열을 모두 섞은 해시 값 반환
// }  // 이 범위 끝
// static size_t map_slot(MapEntry* map, size_t capacity, const char* key) {  // 같은 이름 또는 빈 해시 칸까지 선형 탐색
//     size_t slot = hash_word(key) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     while (map[slot].key && strcmp(map[slot].key, key)) slot = (slot + 1) & (capacity - 1);  // 2의 거듭제곱 크기에 맞춰 비트 AND로 해시 인덱스를 계산
//     return slot;  // 단어를 넣을 해시 칸 반환
// }  // 이 범위 끝
// int solution(const char* message, int** spoiler_ranges, size_t spoiler_ranges_rows, size_t spoiler_ranges_cols) {  // 차분 배열로 가려진 위치를 표시하고 단어를 해시 집합으로 구분하기; 가려진 곳에 등장하면서 완전히 보이는 곳에는 등장하지 않는 서로 다른 단어 수를 세기
//     size_t n = strlen(message), capacity = 1;  // 메시지 길이 / 단어 해시표 칸 수 저장
//     size_t words = 1; for (size_t i = 0; i < n; ++i) if (message[i] == ' ') ++words;  // 해시표 크기를 잡을 단어 수 / 문자 또는 해시 칸 위치 저장
//     while (capacity < 2 * words) capacity *= 2;  // 단어 수의 두 배 이상이 되도록 해시표 크기를 2배씩 늘리기
//     MapEntry* map = calloc(capacity, sizeof(MapEntry));  // 단어별 공개와 가림 상태 공간 확보하고 0으로 시작
//     int* difference = calloc(n + 1, sizeof(int));  // 스포일러 구간의 시작과 끝 변화량 공간 확보하고 0으로 시작
//     for (size_t r = 0; r < spoiler_ranges_rows; ++r) { ++difference[spoiler_ranges[r][0]]; --difference[spoiler_ranges[r][1] + 1]; }  // 구간 시작에서 1을 더하고 끝 다음에서 1을 빼는 차분 배열을 기록
//     int cover = 0; size_t start = 0; bool hidden = false;  // 현재 문자에 겹친 가림 구간 수 / 현재 단어의 시작 / 현재 단어가 한 번이라도 가려졌는지 여부 저장
//     for (size_t i = 0; i <= n; ++i) {  // 문자 또는 해시 칸 위치 순서대로 확인
//         if (i < n) cover += difference[i];  // 메시지 안에서는 차분값을 더해 현재 가려진 구간 수 갱신
//         if (i == n || message[i] == ' ') {  // 공백이나 메시지 끝을 만나면 지금까지 읽은 단어 처리
//             if (i > start) {  // 공백 사이에 글자가 하나라도 있을 때만 단어로 등록
//                 char* word = malloc(i - start + 1); memcpy(word, message + start, i - start); word[i - start] = '\0';  // 공백 사이에서 꺼낸 단어 공간 확보
//                 size_t slot = map_slot(map, capacity, word);  // 단어를 넣을 해시 칸 저장
//                 if (!map[slot].key) map[slot].key = word; else free(word);  // 처음 본 단어면 해시표에 보관하고 중복이면 새로 복사한 문자열 해제
//                 map[slot].value |= hidden ? 2 : 1;  // 단어별 공개와 가림 상태 / 단어를 넣을 해시 칸 / 현재 단어가 한 번이라도 가려졌는지 여부 비트 상태 갱신
//             }  // 이 범위 끝
//             start = i + 1; hidden = false;  // 현재 단어의 시작 / 현재 단어가 한 번이라도 가려졌는지 여부 갱신
//         } else if (cover > 0) hidden = true;  // 앞 조건을 만족하지 않은 경우의 처리를 시작하기
//     }  // 이 범위 끝
//     int answer = 0;  // 공개된 적 없이 가려진 단어 수 저장
//     for (size_t i = 0; i < capacity; ++i) if (map[i].key) { if (map[i].value == 2) ++answer; free((void*)map[i].key); }  // 등록된 단어 중 가려진 적만 있는 상태 2를 세고 저장한 단어 메모리 정리
//     free(map); free(difference);  // 단어별 공개와 가림 상태 / 스포일러 구간의 시작과 끝 변화량 임시 공간 정리
//     return answer;  // 공개된 적 없이 가려진 단어 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 차분 배열로 가려진 위치를 표시하고 단어를 해시 집합으로 구분하기; 가려진 곳에 등장하면서 완전히 보이는 곳에는 등장하지 않는 서로 다른 단어 수를 세기
