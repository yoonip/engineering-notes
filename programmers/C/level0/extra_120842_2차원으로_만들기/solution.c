#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int** solution(int num_list[], size_t num_list_len, int n) {
    size_t rows = num_list_len / n;
    int** answer = malloc(rows * sizeof(*answer));
    for (size_t i = 0; i < rows; ++i) {
        answer[i] = malloc(n * sizeof(**answer));
        for (int j = 0; j < n; ++j) answer[i][j] = num_list[i * n + j];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int** solution(int num_list[], size_t num_list_len, int n) {  // 2차원으로 만들기 풀이 시작
//     size_t rows = num_list_len / n;  // 한 행에 n개씩 넣을 때 필요한 행 수
//     int** answer = malloc(rows * sizeof(*answer));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < rows; ++i) {  // 연속된 n개 원소로 만들 행을 하나씩 생성
//         answer[i] = malloc(n * sizeof(**answer));  // 결과를 저장할 메모리 확보
//         for (int j = 0; j < n; ++j) answer[i][j] = num_list[i * n + j];  // 원본의 i × n 위치부터 n개를 현재 행의 열 순서대로 저장
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 한 행에 n개가 들어가도록 행 공간을 만들고, 원본 인덱스 i × n + j의 값을 i행 j열로 복사.
