#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static size_t hash_name(const char* s) { size_t hash = 5381; while (*s) hash = hash * 33 + (unsigned char)*s++; return hash; }
static int lookup(const char* name, const char** keys, const int* values, size_t cap) {
    size_t at = hash_name(name) & (cap - 1);
    while (keys[at]) { if (!strcmp(keys[at], name)) return values[at]; at = (at + 1) & (cap - 1); }
    return -1;
}
int* solution(const char* enroll[], size_t enroll_len, const char* referral[], size_t referral_len, const char* seller[], size_t seller_len, int amount[], size_t amount_len) {
    (void)referral_len; (void)amount_len; size_t cap = 1; while (cap < enroll_len * 2) cap *= 2;
    const char** keys = calloc(cap, sizeof(*keys)); int* values = malloc(cap * sizeof(*values));
    for (size_t i = 0; i < enroll_len; ++i) { size_t at = hash_name(enroll[i]) & (cap - 1); while (keys[at]) at = (at + 1) & (cap - 1); keys[at] = enroll[i]; values[at] = (int)i; }
    int* parent = malloc(enroll_len * sizeof(*parent)); int* answer = calloc(enroll_len, sizeof(*answer));
    for (size_t i = 0; i < enroll_len; ++i) parent[i] = lookup(referral[i], keys, values, cap);
    for (size_t i = 0; i < seller_len; ++i) {
        int person = lookup(seller[i], keys, values, cap), money = amount[i] * 100;
        while (person >= 0 && money) { int share = money / 10; answer[person] += money - share; money = share; person = parent[person]; }
    }
    free(keys); free(values); free(parent);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// static size_t hash_name(const char* s) { size_t hash = 5381; while (*s) hash = hash * 33 + (unsigned char)*s++; return hash; }  // 판매자 이름으로 해시 만들기
// static int lookup(const char* name, const char** keys, const int* values, size_t cap) {  // 이름 또는 레이블에 대응하는 원래 번호 찾기
//     size_t at = hash_name(name) & (cap - 1);  // 현재 해시 탐색 칸 저장
//     while (keys[at]) { if (!strcmp(keys[at], name)) return values[at]; at = (at + 1) & (cap - 1); }  // 같은 이름을 찾거나 빈 해시 칸을 만날 때까지 다음 칸 확인
//     return -1;  // 조건에 맞는 답이 없으면 -1
// }  // 이 범위 끝
// int* solution(const char* enroll[], size_t enroll_len, const char* referral[], size_t referral_len, const char* seller[], size_t seller_len, int amount[], size_t amount_len) {  // 각 판매의 이익을 본인부터 추천인 방향으로 전달하기; 금액이 단계마다 1/10이 되어 몇 단계 뒤 0이 됨
//     (void)referral_len; (void)amount_len; size_t cap = 1; while (cap < enroll_len * 2) cap *= 2;  // 해시표 크기 갱신
//     const char** keys = calloc(cap, sizeof(*keys)); int* values = malloc(cap * sizeof(*values));  // 이름 해시표의 키 / 해시 칸에 대응하는 가입자 번호 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < enroll_len; ++i) { size_t at = hash_name(enroll[i]) & (cap - 1); while (keys[at]) at = (at + 1) & (cap - 1); keys[at] = enroll[i]; values[at] = (int)i; }  // 가입자 또는 판매 기록 위치 순서대로 확인; 현재 해시 탐색 칸 / 이름 해시표의 키 / 해시 칸에 대응하는 가입자 번호 저장
//     int* parent = malloc(enroll_len * sizeof(*parent)); int* answer = calloc(enroll_len, sizeof(*answer));  // 추천한 상위 판매자 / 가입자별 최종 이익 공간 확보하고 0으로 시작
//     for (size_t i = 0; i < enroll_len; ++i) parent[i] = lookup(referral[i], keys, values, cap);  // 가입자 또는 판매 기록 위치 순서대로 확인; 추천한 상위 판매자 갱신
//     for (size_t i = 0; i < seller_len; ++i) {  // 가입자 또는 판매 기록 위치 순서대로 확인
//         int person = lookup(seller[i], keys, values, cap), money = amount[i] * 100;  // 이익을 나눌 현재 판매자 / 현재 단계에 넘겨진 판매금 저장
//         while (person >= 0 && money) { int share = money / 10; answer[person] += money - share; money = share; person = parent[person]; }  // 추천인이 있고 넘길 돈이 남아 있는 동안 10퍼센트를 위로 전달
//     }  // 이 범위 끝
//     free(keys); free(values); free(parent);  // 이름 해시표의 키 / 해시 칸에 대응하는 가입자 번호 / 추천한 상위 판매자 임시 공간 정리
//     return answer;  // 가입자별 최종 이익 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 판매의 이익을 본인부터 추천인 방향으로 전달하기; 금액이 단계마다 1/10이 되어 몇 단계 뒤 0이 됨
// 예: 1200원은 본인 1080원, 추천인 108원, 그 위 11원, 센터 1원으로 분배됨
// 판매 금액 최대 10000원이므로 기록당 최대 5단계.; 시간 O(가입자 수 + 판매 기록 수), 공간 O(가입자 수)
