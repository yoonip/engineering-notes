#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(int n) {
    char* answer = malloc(12);
    sprintf(answer, "%d", n);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(int n) {  // 문자열로 변환 풀이 시작
//     char* answer = malloc(12);  // 정수의 십진 표기와 끝의 널 문자를 담을 12바이트 공간을 malloc으로 할당
//     sprintf(answer, "%d", n);  // sprintf의 %d 형식으로 n의 십진 표기를 answer 버퍼에 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 문자열을 저장할 공간을 할당한 뒤 sprintf의 %d 형식을 이용해 정수 n을 십진 문자열로 기록
