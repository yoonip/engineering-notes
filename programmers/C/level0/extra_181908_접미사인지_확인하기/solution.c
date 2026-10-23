#include <string.h>

int solution(const char* my_string, const char* is_suffix) {
    size_t n = strlen(my_string), m = strlen(is_suffix);
    return n >= m && strcmp(my_string + n - m, is_suffix) == 0;
}

// 전체 코드 줄별 설명
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// int solution(const char* my_string, const char* is_suffix) {  // 접미사인지 확인하기 풀이 시작
//     size_t n = strlen(my_string), m = strlen(is_suffix);  // strlen으로 원본과 접미사 후보의 길이를 각각 구하기
//     return n >= m && strcmp(my_string + n - m, is_suffix) == 0;  // &&의 단락 평가로 길이를 먼저 확인하고 strcmp로 원본 끝부분과 후보를 비교
// }  // 블록 끝

// 풀이 요약
// 후보가 원본보다 길지 않은지 확인하고 끝부분을 비교
