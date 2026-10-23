#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* str1, const char* str2) { return strstr(str2, str1) != NULL; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* str1, const char* str2) { return strstr(str2, str1) != NULL; }  // 부분 문자열 풀이 시작

// 풀이 요약
// 포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인
