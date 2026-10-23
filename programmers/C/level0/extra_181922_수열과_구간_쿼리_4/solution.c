#include <stdlib.h>
#include <string.h>
#include <stddef.h>

int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {
    (void)queries_cols;
    int* answer = malloc(arr_len * sizeof(int));
    memcpy(answer, arr, arr_len * sizeof(int));
    for (size_t q = 0; q < queries_rows; ++q) {
        int start = queries[q][0], end = queries[q][1], k = queries[q][2];
        for (int i = start; i <= end; ++i) if (k ? i % k == 0 : i == 0) ++answer[i];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {  // 수열과 구간 쿼리 4 풀이 시작
//     (void)queries_cols;  // 사용하지 않는 배열 크기 매개변수를 명시적으로 무시
//     int* answer = malloc(arr_len * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     memcpy(answer, arr, arr_len * sizeof(int));  // memcpy로 입력 정수 배열을 결과 배열에 복사
//     for (size_t q = 0; q < queries_rows; ++q) {  // for로 2차원 쿼리 배열의 각 행을 주어진 순서대로 처리
//         int start = queries[q][0], end = queries[q][1], k = queries[q][2];  // []로 현재 쿼리의 시작, 끝, 배수 기준 k를 읽기
//         for (int i = start; i <= end; ++i) if (k ? i % k == 0 : i == 0) ++answer[i];  // 구간 인덱스를 for로 순회하고 삼항 연산자로 k의 배수를 검사해 해당 원소를 ++로 늘림
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 구간에서 인덱스가 k의 배수인 원소를 1씩 증가
