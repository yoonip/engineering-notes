#include <stdlib.h>
#include <stddef.h>

char* solution(const char* arr[], size_t arr_len) {
    char* answer = malloc(arr_len + 1);
    for (size_t i = 0; i < arr_len; ++i) answer[i] = arr[i][0];
    answer[arr_len] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stddef.h>  // 배열 길이와 인덱스에 쓰는 size_t
//
// char* solution(const char* arr[], size_t arr_len) {  // 문자 리스트를 문자열로 변환하기 풀이 시작
//     char* answer = malloc(arr_len + 1);  // malloc으로 모든 문자와 종료 문자를 담을 공간을 할당
//     for (size_t i = 0; i < arr_len; ++i) answer[i] = arr[i][0];  // for로 문자 배열을 순회하고 각 한 글자 문자열의 첫 문자를 저장
//     answer[arr_len] = '\0';  // 문자열 끝에 널 문자를 넣어 연결 결과를 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열 배열의 원소를 입력 순서대로 연결
