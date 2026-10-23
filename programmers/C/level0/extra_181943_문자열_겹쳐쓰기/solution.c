#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, const char* overwrite_string, int s) {
    char* answer = malloc(strlen(my_string) + 1);
    strcpy(answer, my_string);
    memcpy(answer + s, overwrite_string, strlen(overwrite_string));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, const char* overwrite_string, int s) {  // 문자열 겹쳐쓰기 풀이 시작
//     char* answer = malloc(strlen(my_string) + 1);  // malloc으로 원본 길이와 종료 문자에 필요한 공간을 할당
//     strcpy(answer, my_string);  // strcpy로 종료 문자를 포함한 원본 문자열을 결과 공간에 복사
//     memcpy(answer + s, overwrite_string, strlen(overwrite_string));  // 포인터 덧셈으로 위치 s를 찾아 memcpy로 새 문자열만 덮어쓰기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 시작 위치 s부터 덮어쓸 문자열 길이만큼 교체
