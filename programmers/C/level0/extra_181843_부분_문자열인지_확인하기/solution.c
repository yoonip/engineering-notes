#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* my_string, const char* target) { return strstr(my_string, target) != NULL; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* my_string, const char* target) { return strstr(my_string, target) != NULL; }  // 부분 문자열인지 확인하기 풀이 시작

// 풀이 요약
// target이 my_string 안에 연속해서 나타나는지 검사
