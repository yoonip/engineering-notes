#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string) {
    size_t n = strlen(my_string);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) {
        unsigned char c = (unsigned char)my_string[i];
        answer[i] = isupper(c) ? tolower(c) : toupper(c);
    }
    answer[n] = '\0';
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
// char* solution(const char* my_string) {  // 대문자와 소문자 풀이 시작
//     size_t n = strlen(my_string);  // n에 입력 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) {  // 모든 문자를 순서대로 읽어 대소문자 교환
//         unsigned char c = (unsigned char)my_string[i];  // ctype 함수에 넘길 문자는 unsigned char 범위로 맞추기
//         answer[i] = isupper(c) ? tolower(c) : toupper(c);  // 대문자는 소문자로, 나머지는 대문자로 변환
//     }  // 블록 끝
//     answer[n] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// isupper로 대문자인지 확인해 대문자는 tolower, 소문자는 toupper로 바꿔 저장.
