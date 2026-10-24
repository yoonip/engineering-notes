#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* str1, const char* str2) { return strstr(str1, str2) ? 1 : 2; }

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* str1, const char* str2) { return strstr(str1, str2) ? 1 : 2; }  // strstr로 str2가 str1 안에 있으면 1, 없으면 2 반환

// 풀이 요약
// strstr로 str2가 str1 안에 있으면 1, 없으면 2 반환
