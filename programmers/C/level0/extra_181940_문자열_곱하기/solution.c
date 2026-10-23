#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, int k) {
    size_t n = strlen(my_string);
    char* answer = malloc(n * k + 1);
    for (int i = 0; i < k; ++i) memcpy(answer + n * i, my_string, n);
    answer[n * k] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, int k) {  // 문자열 곱하기 풀이 시작
//     size_t n = strlen(my_string);  // strlen으로 문자열 길이를 구해 size_t형 n에 저장
//     char* answer = malloc(n * k + 1);  // malloc으로 반복한 문자열과 종료 문자 한 개를 담을 공간을 할당
//     for (int i = 0; i < k; ++i) memcpy(answer + n * i, my_string, n);  // for로 반복 위치를 순회하고 memcpy로 각 위치에 원본 문자열을 복사
//     answer[n * k] = '\0';  // 문자열 끝에 널 문자를 넣어 반복 결과를 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 문자열을 k번 순서대로 이어 붙이기
