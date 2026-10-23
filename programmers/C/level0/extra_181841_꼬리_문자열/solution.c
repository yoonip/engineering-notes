#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* str_list[], size_t str_list_len, const char* ex) {
    size_t length = 0;
    for (size_t i = 0; i < str_list_len; ++i) if (!strstr(str_list[i], ex)) length += strlen(str_list[i]);
    char* answer = malloc(length + 1);
    size_t out = 0;
    for (size_t i = 0; i < str_list_len; ++i) if (!strstr(str_list[i], ex)) {
        size_t n = strlen(str_list[i]);
        memcpy(answer + out, str_list[i], n);
        out += n;
    }
    answer[out] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* str_list[], size_t str_list_len, const char* ex) {  // 꼬리 문자열 풀이 시작
//     size_t length = 0;  // ex를 포함하지 않는 문자열들의 전체 문자 수를 저장할 length를 0으로 초기화
//     for (size_t i = 0; i < str_list_len; ++i) if (!strstr(str_list[i], ex)) length += strlen(str_list[i]);  // strstr의 반환값이 NULL인 문자열만 골라 strlen으로 구한 길이를 length에 더하기
//     char* answer = malloc(length + 1);  // 합친 문자열의 전체 길이와 마지막 널 문자 한 칸에 필요한 공간을 할당
//     size_t out = 0;  // answer에서 다음 문자열을 복사할 위치 out을 0으로 초기화
//     for (size_t i = 0; i < str_list_len; ++i) if (!strstr(str_list[i], ex)) {  // 원래 배열 순서대로 순회하며 ex가 포함되지 않은 문자열에 대해서만 복사 블록을 실행
//         size_t n = strlen(str_list[i]);  // 현재 이어 붙일 문자열의 문자 수를 n에 저장
//         memcpy(answer + out, str_list[i], n);  // answer + out 위치에 현재 문자열의 문자 n개를 memcpy로 복사
//         out += n;  // 복사한 길이 n만큼 out을 늘려 다음 문자열을 붙일 위치로 이동
//     }  // 블록 끝
//     answer[out] = '\0';  // 마지막 복사 위치에 널 문자를 넣어 결과를 유효한 C 문자열로 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// strstr로 ex의 포함 여부를 검사. 포함하지 않는 문자열들의 총길이를 먼저 구해 공간을 할당한 뒤, 같은 조건으로 다시 순회하며 원래 순서대로 복사
