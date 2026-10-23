#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* rny_string) {
    size_t n = strlen(rny_string), length = n;
    for (size_t i = 0; i < n; ++i) if (rny_string[i] == 'm') ++length;
    char* answer = malloc(length + 1);
    size_t out = 0;
    for (size_t i = 0; i < n; ++i) {
        if (rny_string[i] == 'm') { answer[out++] = 'r'; answer[out++] = 'n'; }
        else answer[out++] = rny_string[i];
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
// char* solution(const char* rny_string) {  // rny_string 풀이 시작
//     size_t n = strlen(rny_string), length = n;  // 원래 문자 수 n을 구하고 결과 길이 length도 우선 n으로 시작
//     for (size_t i = 0; i < n; ++i) if (rny_string[i] == 'm') ++length;  // m은 rn 두 글자가 되므로 m마다 필요한 길이를 1씩 추가
//     char* answer = malloc(length + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; i < n; ++i) {  // 원래 문자열을 앞에서부터 읽으며 m을 치환
//         if (rny_string[i] == 'm') { answer[out++] = 'r'; answer[out++] = 'n'; }  // m을 만나면 결과에 r과 n을 차례로 넣기
//         else answer[out++] = rny_string[i];  // m이 아니면 원래 문자를 그대로 복사
//     }  // 블록 끝
//     answer[out] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 한 문자 m을 두 문자 rn으로 모두 치환
