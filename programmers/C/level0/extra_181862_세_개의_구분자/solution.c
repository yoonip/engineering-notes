#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

static bool separator(char c) { return c == 'a' || c == 'b' || c == 'c'; }
char** solution(const char* myStr) {
    size_t count = 0;
    for (size_t i = 0; myStr[i]; ) {
        while (separator(myStr[i])) ++i;
        if (!myStr[i]) break;
        ++count;
        while (myStr[i] && !separator(myStr[i])) ++i;
    }
    char** answer = malloc((count ? count : 1) * sizeof(char*));
    if (!count) {
        answer[0] = malloc(6);
        strcpy(answer[0], "EMPTY");
        return answer;
    }
    size_t out = 0;
    for (size_t i = 0; myStr[i]; ) {
        while (separator(myStr[i])) ++i;
        if (!myStr[i]) break;
        size_t start = i;
        while (myStr[i] && !separator(myStr[i])) ++i;
        size_t n = i - start;
        answer[out] = malloc(n + 1);
        memcpy(answer[out], myStr + start, n);
        answer[out++][n] = '\0';
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
// static bool separator(char c) { return c == 'a' || c == 'b' || c == 'c'; }  // bool 보조 함수에서 a·b·c인지 논리합으로 판별
// char** solution(const char* myStr) {  // 세 개의 구분자 풀이 시작
//     size_t count = 0;  // a·b·c로 구분한 뒤 남는 빈칸 아닌 조각 수를 0으로 시작
//     for (size_t i = 0; myStr[i]; ) {  // 문자열 끝까지 구분자와 일반 문자열 조각을 번갈아 탐색
//         while (separator(myStr[i])) ++i;  // 연속된 구분자 a·b·c를 모두 건너뜀
//         if (!myStr[i]) break;  // 구분자를 건너뛴 뒤 문자열이 끝나면 탐색 종료
//         ++count;  // 새로 발견한 빈칸 아닌 조각 하나를 셈
//         while (myStr[i] && !separator(myStr[i])) ++i;  // 다음 구분자나 문자열 끝까지 현재 조각의 끝 탐색
//     }  // 블록 끝
//     char** answer = malloc((count ? count : 1) * sizeof(char*));  // answer를 저장할 메모리 확보
//     if (!count) {  // 나눠진 문자열이 하나도 없으면 EMPTY 하나를 반환
//         answer[0] = malloc(6);  // 결과를 저장할 메모리 확보
//         strcpy(answer[0], "EMPTY");  // strcpy로 종료 문자까지 문자열을 목적지에 복사
//         return answer;  // 완성한 결과 반환
//     }  // 블록 끝
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; myStr[i]; ) {  // 문자열 끝까지 구분자와 일반 문자열 조각을 번갈아 탐색
//         while (separator(myStr[i])) ++i;  // 연속된 구분자 a·b·c를 모두 건너뜀
//         if (!myStr[i]) break;  // 구분자를 건너뛴 뒤 문자열이 끝나면 탐색 종료
//         size_t start = i;  // 이번 문자열 조각의 시작 위치 기억
//         while (myStr[i] && !separator(myStr[i])) ++i;  // 다음 구분자나 문자열 끝까지 현재 조각의 끝 탐색
//         size_t n = i - start;  // 현재 문자열 조각의 시작·끝 차이로 길이 계산
//         answer[out] = malloc(n + 1);  // 결과를 저장할 메모리 확보
//         memcpy(answer[out], myStr + start, n);  // 구분자를 제외한 현재 조각의 문자 n개 복사
//         answer[out++][n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// a·b·c를 구분자로 건너뛰며 그 사이의 빈칸 아닌 문자열만 복사. 남는 조각이 하나도 없으면 EMPTY 하나 반환.
