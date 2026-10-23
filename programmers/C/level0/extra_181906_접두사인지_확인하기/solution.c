#include <string.h>

int solution(const char* my_string, const char* is_prefix) {
    return strncmp(my_string, is_prefix, strlen(is_prefix)) == 0;
}

// 전체 코드 줄별 설명
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// int solution(const char* my_string, const char* is_prefix) {  // 접두사인지 확인하기 풀이 시작
//     return strncmp(my_string, is_prefix, strlen(is_prefix)) == 0;  // strncmp로 접두사 후보 길이만큼 비교하고 결과가 0인지 반환
// }  // 블록 끝

// 풀이 요약
// 원본의 시작 부분과 접두사 후보를 비교
