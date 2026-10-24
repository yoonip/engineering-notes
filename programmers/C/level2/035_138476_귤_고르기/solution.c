#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int ascending(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }
static int descending(const void* p, const void* q) { return *(const int*)q - *(const int*)p; }
int solution(int k, int tangerine[], size_t tangerine_len) {
    int* sorted = malloc(tangerine_len * sizeof(*sorted)); int* counts = calloc(tangerine_len, sizeof(*counts));
    memcpy(sorted, tangerine, tangerine_len * sizeof(*sorted)); qsort(sorted, tangerine_len, sizeof(*sorted), ascending);
    size_t kinds = 0;
    for (size_t i = 0; i < tangerine_len; ++i) {
        if (!i || sorted[i] != sorted[i - 1]) ++kinds;
        ++counts[kinds - 1];
    }
    qsort(counts, kinds, sizeof(*counts), descending); int answer = 0;
    while (k > 0) k -= counts[answer++];
    free(sorted); free(counts);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static int ascending(const void* p, const void* q) { return *(const int*)p - *(const int*)q; }  // 작은 값부터 정렬
// static int descending(const void* p, const void* q) { return *(const int*)q - *(const int*)p; }  // 큰 값부터 정렬
// int solution(int k, int tangerine[], size_t tangerine_len) {  // 크기별 개수를 내림차순으로 정렬해 많은 종류부터 고르면 같은 종류 수로 가장 많은 귤을 담을 수 있음
//     int* sorted = malloc(tangerine_len * sizeof(*sorted)); int* counts = calloc(tangerine_len, sizeof(*counts));  // 크기순 귤 사본 / 각 귤 크기의 개수 공간 확보하고 0으로 시작
//     memcpy(sorted, tangerine, tangerine_len * sizeof(*sorted)); qsort(sorted, tangerine_len, sizeof(*sorted), ascending);  // 크기순 귤 사본 정렬 순서 맞추기
//     size_t kinds = 0;  // 서로 다른 귤 크기 수 저장
//     for (size_t i = 0; i < tangerine_len; ++i) {  // 같은 크기 귤을 묶을 위치 순서대로 확인
//         if (!i || sorted[i] != sorted[i - 1]) ++kinds;  // 첫 귤이거나 앞 귤과 크기가 다르면 새 크기 종류로 세기
//         ++counts[kinds - 1];  // 각 귤 크기의 개수 갱신
//     }  // 이 범위 끝
//     qsort(counts, kinds, sizeof(*counts), descending); int answer = 0;  // 각 귤 크기의 개수 / 서로 다른 귤 크기 수 정렬 순서 맞추기
//     while (k > 0) k -= counts[answer++];  // 앞으로 담아야 할 귤 수가 0보다 크면 반복; 상자에 담은 귤 종류 수 갱신
//     free(sorted); free(counts);  // 크기순 귤 사본 / 각 귤 크기의 개수 임시 공간 정리
//     return answer;  // 상자에 담은 귤 종류 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 크기별 개수를 내림차순으로 정렬해 많은 종류부터 고르면 같은 종류 수로 가장 많은 귤을 담을 수 있음
// 예: k=6이면 개수 2,2,2인 세 종류 선택; 귤 N개·크기 U종류일 때 시간 O(N+U log U), 공간 O(U)
