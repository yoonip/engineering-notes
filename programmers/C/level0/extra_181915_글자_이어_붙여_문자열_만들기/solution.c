#include <stdlib.h>
#include <stddef.h>

char* solution(const char* my_string, int index_list[], size_t index_list_len) {
    char* answer = malloc(index_list_len + 1);
    for (size_t i = 0; i < index_list_len; ++i) answer[i] = my_string[index_list[i]];
    answer[index_list_len] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(const char* my_string, int index_list[], size_t index_list_len) {  // 글자 이어 붙여 문자열 만들기 풀이 시작
//     char* answer = malloc(index_list_len + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     for (size_t i = 0; i < index_list_len; ++i) answer[i] = my_string[index_list[i]];  // for로 인덱스 목록을 순회하고 중첩 []로 선택한 문자를 결과에 저장
//     answer[index_list_len] = '\0';  // 결과의 마지막 위치에 널 문자를 넣어 C 문자열을 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 주어진 인덱스 순서대로 원본 문자를 연결
