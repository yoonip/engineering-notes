#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int* solution(int rows, int columns, int** queries, size_t queries_rows, size_t queries_cols) {
    (void)queries_cols;
    int* board = malloc((size_t)rows * columns * sizeof(*board));
    int* answer = malloc(queries_rows * sizeof(*answer));
    for (int i = 0; i < rows * columns; ++i) board[i] = i + 1;
    for (size_t i = 0; i < queries_rows; ++i) {
        int top = queries[i][0] - 1, left = queries[i][1] - 1, bottom = queries[i][2] - 1, right = queries[i][3] - 1;
        int previous = board[top * columns + left], minimum = previous;
        for (int c = left + 1; c <= right; ++c) {
            int index = top * columns + c, current = board[index];
            board[index] = previous; previous = current; if (current < minimum) minimum = current;
        }
        for (int r = top + 1; r <= bottom; ++r) {
            int index = r * columns + right, current = board[index];
            board[index] = previous; previous = current; if (current < minimum) minimum = current;
        }
        for (int c = right - 1; c >= left; --c) {
            int index = bottom * columns + c, current = board[index];
            board[index] = previous; previous = current; if (current < minimum) minimum = current;
        }
        for (int r = bottom - 1; r >= top; --r) {
            int index = r * columns + left, current = board[index];
            board[index] = previous; previous = current; if (current < minimum) minimum = current;
        }
        answer[i] = minimum;
    }
    free(board);
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
// int* solution(int rows, int columns, int** queries, size_t queries_rows, size_t queries_cols) {  // 테두리 좌표를 시계 방향으로 모은 뒤 각 칸에 직전 칸의 기존 값을 넣기; 안쪽 값은 경로에 포함되지 않음
//     (void)queries_cols;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int* board = malloc((size_t)rows * columns * sizeof(*board));  // 회전 중인 행렬 공간 확보
//     int* answer = malloc(queries_rows * sizeof(*answer));  // 회전마다 옮긴 값의 최솟값 공간 확보
//     for (int i = 0; i < rows * columns; ++i) board[i] = i + 1;  // 회전 질의 번호 순서대로 확인; 회전 중인 행렬 갱신
//     for (size_t i = 0; i < queries_rows; ++i) {  // 회전 질의 번호 순서대로 확인
//         int top = queries[i][0] - 1, left = queries[i][1] - 1, bottom = queries[i][2] - 1, right = queries[i][3] - 1;  // 회전 영역 위 행 / 회전 영역 왼쪽 열 / 회전 영역 아래 행 / 회전 영역 오른쪽 열 저장
//         int previous = board[top * columns + left], minimum = previous;  // 다음 칸에 넘길 이전 값 / 이번 테두리의 최솟값 저장
//         for (int c = left + 1; c <= right; ++c) {  // 테두리의 열 순서대로 확인
//             int index = top * columns + c, current = board[index];  // 옮길 칸의 일차원 위치 / 덮어쓰기 전 칸 값 저장
//             board[index] = previous; previous = current; if (current < minimum) minimum = current;  // 회전 중인 행렬 / 다음 칸에 넘길 이전 값 / 이번 테두리의 최솟값 갱신
//         }  // 이 범위 끝
//         for (int r = top + 1; r <= bottom; ++r) {  // 테두리의 행 순서대로 확인
//             int index = r * columns + right, current = board[index];  // 옮길 칸의 일차원 위치 / 덮어쓰기 전 칸 값 저장
//             board[index] = previous; previous = current; if (current < minimum) minimum = current;  // 회전 중인 행렬 / 다음 칸에 넘길 이전 값 / 이번 테두리의 최솟값 갱신
//         }  // 이 범위 끝
//         for (int c = right - 1; c >= left; --c) {  // 테두리의 열 순서대로 확인
//             int index = bottom * columns + c, current = board[index];  // 옮길 칸의 일차원 위치 / 덮어쓰기 전 칸 값 저장
//             board[index] = previous; previous = current; if (current < minimum) minimum = current;  // 회전 중인 행렬 / 다음 칸에 넘길 이전 값 / 이번 테두리의 최솟값 갱신
//         }  // 이 범위 끝
//         for (int r = bottom - 1; r >= top; --r) {  // 테두리의 행 순서대로 확인
//             int index = r * columns + left, current = board[index];  // 옮길 칸의 일차원 위치 / 덮어쓰기 전 칸 값 저장
//             board[index] = previous; previous = current; if (current < minimum) minimum = current;  // 회전 중인 행렬 / 다음 칸에 넘길 이전 값 / 이번 테두리의 최솟값 갱신
//         }  // 이 범위 끝
//         answer[i] = minimum;  // 회전마다 옮긴 값의 최솟값 갱신
//     }  // 이 범위 끝
//     free(board);  // 회전 중인 행렬 임시 공간 정리
//     return answer;  // 회전마다 옮긴 값의 최솟값 반환
// }  // 이 범위 끝

// 풀이 요약
// 테두리 좌표를 시계 방향으로 모은 뒤 각 칸에 직전 칸의 기존 값을 넣기; 안쪽 값은 경로에 포함되지 않음
// 예: 첫 6×6 예제의 회전별 최솟값은 [8,10,25].; 회전 Q개일 때 시간 O(행*열+Q(행+열)), 공간 O(행*열+Q)
