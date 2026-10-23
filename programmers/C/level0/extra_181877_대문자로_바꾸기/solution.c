#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* myString) {
    size_t n = strlen(myString);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) answer[i] = toupper((unsigned char)myString[i]);
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
// char* solution(const char* myString) {  // 대문자로 바꾸기 풀이 시작
//     size_t n = strlen(myString);  // 대문자로 바꿀 입력 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) answer[i] = toupper((unsigned char)myString[i]);  // for로 문자를 순회하고 대소문자 변환 결과를 지정한 위치에 저장
//     answer[n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 문자를 toupper에 넘겨 대문자로 바꾼 뒤 새 문자열에 저장.
