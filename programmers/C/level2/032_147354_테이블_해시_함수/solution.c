#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int sort_column;
static int compare(const void* p, const void* q) {
    const int* a = *(const int* const*)p; const int* b = *(const int* const*)q;
    if (a[sort_column] != b[sort_column]) return (a[sort_column] > b[sort_column]) - (a[sort_column] < b[sort_column]);
    return (b[0] > a[0]) - (b[0] < a[0]);
}
int solution(int** data, size_t data_rows, size_t data_cols, int col, int row_begin, int row_end) {
    int** rows = malloc(data_rows * sizeof(*rows)); memcpy(rows, data, data_rows * sizeof(*rows));
    sort_column = col - 1; qsort(rows, data_rows, sizeof(*rows), compare); int answer = 0;
    for (int index = row_begin; index <= row_end; ++index) {
        int value = 0;
        for (size_t j = 0; j < data_cols; ++j) value += rows[index - 1][j] % index;
        answer ^= value;
    }
    free(rows);
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
// static int sort_column;  // 정렬 기준 열 번호 확인
// static int compare(const void* p, const void* q) {  // 지정 열 오름차순, 같은 값이면 첫 열 내림차순 비교
//     const int* a = *(const int* const*)p; const int* b = *(const int* const*)q;  // 비교할 첫 행 / 비교할 둘째 행 저장
//     if (a[sort_column] != b[sort_column]) return (a[sort_column] > b[sort_column]) - (a[sort_column] < b[sort_column]);  // 지정 열 값이 다르면 그 열을 기준으로 오름차순 비교
//     return (b[0] > a[0]) - (b[0] < a[0]);  // 비교할 둘째 행 / 비교할 첫 행로 최종값 계산
// }  // 이 범위 끝
// int solution(int** data, size_t data_rows, size_t data_cols, int col, int row_begin, int row_end) {  // 지정 열 오름차순·기본키 내림차순으로 정렬하고, 각 행 번호로 나눈 나머지 합을 XOR하기
//     int** rows = malloc(data_rows * sizeof(*rows)); memcpy(rows, data, data_rows * sizeof(*rows));  // 정렬할 행 포인터 사본 공간 확보
//     sort_column = col - 1; qsort(rows, data_rows, sizeof(*rows), compare); int answer = 0;  // 정렬 기준 열 번호 / 정렬할 행 포인터 사본 정렬 순서 맞추기
//     for (int index = row_begin; index <= row_end; ++index) {  // 해시에 포함할 1부터 시작하는 행 번호 순서대로 확인
//         int value = 0;  // 현재 행을 행 번호로 나눈 나머지 합 저장
//         for (size_t j = 0; j < data_cols; ++j) value += rows[index - 1][j] % index;  // 나머지를 더할 열 순서대로 확인; 현재 행을 행 번호로 나눈 나머지 합 / 정렬할 행 포인터 사본 / 해시에 포함할 1부터 시작하는 행 번호 더해 누적
//         answer ^= value;  // 행별 나머지 합의 XOR / 현재 행을 행 번호로 나눈 나머지 합 XOR 누적
//     }  // 이 범위 끝
//     free(rows);  // 정렬할 행 포인터 사본 임시 공간 정리
//     return answer;  // 행별 나머지 합의 XOR 반환
// }  // 이 범위 끝

// 풀이 요약
// 지정 열 오름차순·기본키 내림차순으로 정렬하고, 각 행 번호로 나눈 나머지 합을 XOR하기
// 예: 정렬 후 S2=0,S3=4이므로 0 XOR 4=4; N행·M열일 때 시간 O(N log N+NM), 정렬 공간 O(N)
