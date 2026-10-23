#include <stdlib.h>
#include <stddef.h>

int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {
    (void)arr_len;
    (void)queries_cols;
    int* answer = malloc(queries_rows * sizeof(int));
    for (size_t q = 0; q < queries_rows; ++q) {
        int best = -1;
        for (int i = queries[q][0]; i <= queries[q][1]; ++i) {
            if (arr[i] > queries[q][2] && (best == -1 || arr[i] < best)) best = arr[i];
        }
        answer[q] = best;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {  // 수열과 구간 쿼리 2 풀이 시작
//     (void)arr_len;  // 사용하지 않는 배열 크기 매개변수를 명시적으로 무시
//     (void)queries_cols;  // 사용하지 않는 배열 크기 매개변수를 명시적으로 무시
//     int* answer = malloc(queries_rows * sizeof(int));  // malloc으로 결과 정수 배열을 할당하며 sizeof(int)로 한 원소의 바이트 수를 구하기
//     for (size_t q = 0; q < queries_rows; ++q) {  // for로 2차원 쿼리 배열의 각 행을 주어진 순서대로 처리
//         int best = -1;  // 조건을 만족하는 값이 없음을 나타내는 -1로 최솟값 후보를 초기화
//         for (int i = queries[q][0]; i <= queries[q][1]; ++i) {  // for에서 <=를 사용해 쿼리의 시작 인덱스부터 끝 인덱스까지 포함해 검사
//             if (arr[i] > queries[q][2] && (best == -1 || arr[i] < best)) best = arr[i];  // &&와 ||로 기준보다 크고 기존 후보보다 작은 값을 골라 최솟값 후보를 갱신
//         }  // 블록 끝
//         answer[q] = best;  // 현재 쿼리에서 찾은 최솟값 또는 -1을 결과 배열에 저장
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 구간에서 k보다 큰 값 중 최솟값을 찾고, 없으면 -1을 기록
