#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* myString) {
    size_t n = strlen(myString);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) {
        char c = tolower((unsigned char)myString[i]);
        answer[i] = c == 'a' ? 'A' : c;
    }
    answer[n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* myString) {  // A 강조하기 풀이 시작
//     size_t n = strlen(myString);  // 변환할 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) {  // 모든 문자를 차례로 변환
//         char c = tolower((unsigned char)myString[i]);  // 현재 문자를 우선 소문자로 통일
//         answer[i] = c == 'a' ? 'A' : c;  // 소문자 a만 대문자 A로 바꾸고 다른 소문자는 그대로 저장
//     }  // 블록 끝
//     answer[n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됨
