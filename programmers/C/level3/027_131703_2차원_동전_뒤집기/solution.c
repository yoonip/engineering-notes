#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <stdint.h>

int solution(int** beginning, size_t beginning_rows, size_t beginning_cols, int** target, size_t target_rows, size_t target_cols) {
    (void)target_rows; (void)target_cols; int flips = 0;
    for (size_t r = 0; r < beginning_rows; ++r) flips += beginning[r][0] ^ target[r][0] ^ beginning[0][0] ^ target[0][0];
    for (size_t c = 0; c < beginning_cols; ++c) flips += beginning[0][c] ^ target[0][c];
    for (size_t r = 0; r < beginning_rows; ++r) for (size_t c = 0; c < beginning_cols; ++c)
        if ((beginning[r][0] ^ target[r][0] ^ beginning[0][0] ^ target[0][0] ^ beginning[0][c] ^ target[0][c]) != (beginning[r][c] ^ target[r][c])) return -1;
    int reverse = (int)(beginning_rows + beginning_cols) - flips;
    return flips < reverse ? flips : reverse;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <stdint.h>  // 비트 마스크와 해시 키에 쓸 고정 폭 정수
//
// int solution(int** beginning, size_t beginning_rows, size_t beginning_cols, int** target, size_t target_rows, size_t target_cols) {  // 각 칸의 변화 여부는 행 뒤집기와 열 뒤집기의 XOR입니다. 첫 행을 뒤집지 않는다고 고정하면 나머지 행과 열의 선택이 결정됩니다.
//     (void)target_rows; (void)target_cols; int flips = 0;  // 한 가지 행열 뒤집기 횟수 갱신
//     for (size_t r = 0; r < beginning_rows; ++r) flips += beginning[r][0] ^ target[r][0] ^ beginning[0][0] ^ target[0][0];  // 확인할 행 순서대로 확인; 한 가지 행열 뒤집기 횟수 / 확인할 행 더해 누적
//     for (size_t c = 0; c < beginning_cols; ++c) flips += beginning[0][c] ^ target[0][c];  // 확인할 열 순서대로 확인; 한 가지 행열 뒤집기 횟수 / 확인할 열 더해 누적
//     for (size_t r = 0; r < beginning_rows; ++r) for (size_t c = 0; c < beginning_cols; ++c)  // 확인할 행 순서대로 확인; 확인할 열 갱신
//         if ((beginning[r][0] ^ target[r][0] ^ beginning[0][0] ^ target[0][0] ^ beginning[0][c] ^ target[0][c]) != (beginning[r][c] ^ target[r][c])) return -1;  // 첫 행·열로 정한 뒤집기와 어느 칸의 목표가 어긋나면 불가능
//     int reverse = (int)(beginning_rows + beginning_cols) - flips;  // 모든 선택을 반대로 했을 때 횟수 저장
//     return flips < reverse ? flips : reverse;  // 한 가지 행열 뒤집기 횟수 / 모든 선택을 반대로 했을 때 횟수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 각 칸의 변화 여부는 행 뒤집기와 열 뒤집기의 XOR입니다. 첫 행을 뒤집지 않는다고 고정하면 나머지 행과 열의 선택이 결정됩니다.
// 결정한 선택이 모든 칸의 목표와 일치하는지 검사합니다. 가능하다면 그 선택과 모든 행·열의 선택을 반대로 한 경우 중 더 적은 횟수를 고릅니다. N행 M열에 대해 시간은 O(NM), 이 C 구현의 추가 공간은 O(1)입니다.
// 예를 들어 한 해법이 행 2개와 열 3개를 뒤집으면 비용은 5입니다. 모든 선택을 반대로 한 해법의 비용은 N+M-5입니다.
