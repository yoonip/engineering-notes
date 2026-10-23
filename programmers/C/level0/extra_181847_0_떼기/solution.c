#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* n_str) {
    while (*n_str == '0') ++n_str;
    char* answer = malloc(strlen(n_str) + 1);
    strcpy(answer, n_str);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* n_str) {  // 0 떼기 풀이 시작
//     while (*n_str == '0') ++n_str;  // 현재 문자를 *로 읽고 '0'인 동안 포인터 n_str을 다음 문자로 이동해 앞부분의 0을 건너뜀
//     char* answer = malloc(strlen(n_str) + 1);  // 남은 문자열 길이에 널 문자 한 칸을 더한 공간을 malloc으로 할당
//     strcpy(answer, n_str);  // strcpy로 0을 건너뛴 위치부터 문자열 끝의 널 문자까지 answer에 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 포인터를 앞부분의 연속된 0 뒤로 옮긴 뒤, 남은 문자열을 새 공간에 복사해 반환.
