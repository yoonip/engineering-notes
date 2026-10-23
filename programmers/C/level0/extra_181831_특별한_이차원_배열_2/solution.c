#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int** arr, size_t arr_rows, size_t arr_cols) {
    for (size_t i = 0; i < arr_rows; ++i)
        for (size_t j = i + 1; j < arr_cols; ++j) if (arr[i][j] != arr[j][i]) return 0;
    return 1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int** arr, size_t arr_rows, size_t arr_cols) {  // 특별한 이차원 배열 2 풀이 시작
//     for (size_t i = 0; i < arr_rows; ++i)  // 비교할 첫 번째 좌표의 행 번호 i를 모든 행에 대해 순회
//         for (size_t j = i + 1; j < arr_cols; ++j) if (arr[i][j] != arr[j][i]) return 0;  // 주대각선 위쪽의 j > i인 칸만 순회하며 대칭 위치 arr[j][i]와 다르면 즉시 0을 반환
//     return 1;  // 모든 대칭 위치의 값이 같으면 대칭 배열을 뜻하는 1을 반환
// }  // 블록 끝

// 풀이 요약
// 정사각형 배열의 주대각선 위쪽 칸 arr[i][j]와 아래쪽의 대칭 칸 arr[j][i]를 한 번씩 비교. 하나라도 다르면 0, 모두 같으면 1을 반환
