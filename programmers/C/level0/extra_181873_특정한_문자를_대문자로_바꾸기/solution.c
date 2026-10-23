#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* my_string, const char* alp) {
    size_t n = strlen(my_string);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) answer[i] = my_string[i] == alp[0] ? toupper((unsigned char)my_string[i]) : my_string[i];
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
// char* solution(const char* my_string, const char* alp) {  // 특정한 문자를 대문자로 바꾸기 풀이 시작
//     size_t n = strlen(my_string);  // 선택한 문자만 대문자로 바꿀 문자열의 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) answer[i] = my_string[i] == alp[0] ? toupper((unsigned char)my_string[i]) : my_string[i];  // for로 문자를 순회하고 대소문자 변환 결과를 지정한 위치에 저장
//     answer[n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 지정된 문자만 대문자로 치환
