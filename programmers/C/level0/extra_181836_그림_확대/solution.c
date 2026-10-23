#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char** solution(const char* picture[], size_t picture_len, int k) {
    char** answer = malloc(picture_len * k * sizeof(char*));
    for (size_t i = 0; i < picture_len; ++i) {
        size_t n = strlen(picture[i]);
        for (int r = 0; r < k; ++r) {
            char* row = malloc(n * k + 1);
            for (size_t j = 0; j < n; ++j) for (int c = 0; c < k; ++c) row[j * k + c] = picture[i][j];
            row[n * k] = '\0';
            answer[i * k + r] = row;
        }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char** solution(const char* picture[], size_t picture_len, int k) {  // 그림 확대 풀이 시작
//     char** answer = malloc(picture_len * k * sizeof(char*));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < picture_len; ++i) {  // 원본 그림의 각 행을 순서대로 확대
//         size_t n = strlen(picture[i]);  // 원본 그림에서 현재 행의 문자 수 저장
//         for (int r = 0; r < k; ++r) {  // 같은 확대 행을 세로로 k번 생성
//             char* row = malloc(n * k + 1);  // row를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//             for (size_t j = 0; j < n; ++j) for (int c = 0; c < k; ++c) row[j * k + c] = picture[i][j];  // 각 문자를 가로로 k번 복사해 확대된 한 행 채우기
//             row[n * k] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//             answer[i * k + r] = row;  // 원본 i행에서 생성한 r번째 확대 행의 주소를 결과에 연결
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 문자를 k번 반복해 가로 확대하고 완성된 행을 k번 반복해 세로 확대
