#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

static int compare(const void* p, const void* q) { int a = *(const int*)p, b = *(const int*)q; return (a > b) - (a < b); }
int solution(int A[], size_t A_len, int B[], size_t B_len) {
    int* a = malloc(A_len * sizeof(*a)); int* b = malloc(B_len * sizeof(*b));
    memcpy(a, A, A_len * sizeof(*a)); memcpy(b, B, B_len * sizeof(*b));
    qsort(a, A_len, sizeof(*a), compare); qsort(b, B_len, sizeof(*b), compare);
    size_t wins = 0;
    for (size_t i = 0; i < B_len; ++i) if (wins < A_len && b[i] > a[wins]) ++wins;
    free(a); free(b);
    return (int)wins;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// static int compare(const void* p, const void* q) { int a = *(const int*)p, b = *(const int*)q; return (a > b) - (a < b); }  // 팀 점수를 작은 값부터 정렬
// int solution(int A[], size_t A_len, int B[], size_t B_len) {  // B의 작은 숫자로 이길 수 있는 가장 작은 A부터 이긴다; 못 이기는 B는 어떤 남은 상대도 이길 수 없으므로 승리 후보에서 버려도 됨
//     int* a = malloc(A_len * sizeof(*a)); int* b = malloc(B_len * sizeof(*b));  // A팀의 오름차순 점수 / B팀의 오름차순 점수 공간 확보
//     memcpy(a, A, A_len * sizeof(*a)); memcpy(b, B, B_len * sizeof(*b));  // A팀의 오름차순 점수 / B팀의 오름차순 점수 복사
//     qsort(a, A_len, sizeof(*a), compare); qsort(b, B_len, sizeof(*b), compare);  // A팀의 오름차순 점수 / B팀의 오름차순 점수 정렬 순서 맞추기
//     size_t wins = 0;  // 이긴 A팀 선수 수이자 다음 상대 저장
//     for (size_t i = 0; i < B_len; ++i) if (wins < A_len && b[i] > a[wins]) ++wins;  // B의 숫자로 이길 수 있는 가장 작은 A를 하나씩 소비
//     free(a); free(b);  // A팀의 오름차순 점수 / B팀의 오름차순 점수 임시 공간 정리
//     return (int)wins;  // 이긴 A팀 선수 수이자 다음 상대로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// B의 작은 숫자로 이길 수 있는 가장 작은 A부터 이긴다; 못 이기는 B는 어떤 남은 상대도 이길 수 없으므로 승리 후보에서 버려도 됨
// 예: 정렬한 A=[1,3,5,7], B=[2,2,6,8]은 2>1, 6>3, 8>5로 세 번 승리하기; 남은 숫자끼리는 패배 경기로 배치하면 됨
// 매칭할 A의 원래 순서는 그 상대 위치에 B를 배치하면 되므로 정렬해도 최대 승점은 같음; 시간 O(N log N), 공간 O(N)
