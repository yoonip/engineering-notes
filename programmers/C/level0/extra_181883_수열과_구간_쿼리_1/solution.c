#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {
    int* answer = malloc(arr_len * sizeof(int));
    memcpy(answer, arr, arr_len * sizeof(int));
    for (size_t q = 0; q < queries_rows; ++q)
        for (int i = queries[q][0]; i <= queries[q][1]; ++i) ++answer[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int** queries, size_t queries_rows, size_t queries_cols) {  // 수열과 구간 쿼리 1 풀이 시작
//     int* answer = malloc(arr_len * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, arr, arr_len * sizeof(int));  // memcpy로 지정한 바이트 수만큼 원소를 목적지에 복사
//     for (size_t q = 0; q < queries_rows; ++q)  // 입력 순서대로 각 구간 증가 쿼리 적용
//         for (int i = queries[q][0]; i <= queries[q][1]; ++i) ++answer[i];  // 쿼리의 시작·끝 인덱스를 포함해 구간의 모든 값에 1 더하기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 닫힌 구간에 속한 원소를 모두 1씩 증가
