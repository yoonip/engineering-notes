#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

static char* copy_text(const char* text) {
    char* result = malloc(strlen(text) + 1);
    strcpy(result, text);
    return result;
}
char** solution(const char* names[], size_t names_len) {
    size_t length = (names_len + 4) / 5;
    char** answer = malloc(length * sizeof(char*));
    for (size_t i = 0; i < length; ++i) answer[i] = copy_text(names[i * 5]);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// static char* copy_text(const char* text) {  // const char*로 받은 문자열을 복사해 새 포인터를 반환할 보조 함수를 정의
//     char* result = malloc(strlen(text) + 1);  // result를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     strcpy(result, text);  // strcpy로 종료 문자까지 문자열을 목적지에 복사
//     return result;  // 새로 할당해 복사한 문자열의 주소 반환
// }  // 블록 끝
// char** solution(const char* names[], size_t names_len) {  // 5명씩 풀이 시작
//     size_t length = (names_len + 4) / 5;  // 결과의 원소 수 저장
//     char** answer = malloc(length * sizeof(char*));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < length; ++i) answer[i] = copy_text(names[i * 5]);  // 각 다섯 명 묶음의 첫 사람인 인덱스 0, 5, 10, …의 이름 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝// 풀이 요약
// 각 그룹의 첫 위치는 0, 5, 10 순서임. 마지막 소규모 그룹도 자동 포함됨
