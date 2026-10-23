#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string, int num1, int num2) {
    char* answer = malloc(strlen(my_string) + 1);
    strcpy(answer, my_string);
    char temp = answer[num1]; answer[num1] = answer[num2]; answer[num2] = temp;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// char* solution(const char* my_string, int num1, int num2) {  // 인덱스 바꾸기 풀이 시작
//     char* answer = malloc(strlen(my_string) + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     strcpy(answer, my_string);  // strcpy는 종료 문자까지 포함하여 문자열을 결과 공간에 복사
//     char temp = answer[num1]; answer[num1] = answer[num2]; answer[num2] = temp;  // num1 위치의 문자를 임시 저장하고 두 위치의 문자를 서로 교환
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 원본 문자열을 복사하고 임시 문자 하나를 이용해 num1·num2 위치의 문자를 교환.
