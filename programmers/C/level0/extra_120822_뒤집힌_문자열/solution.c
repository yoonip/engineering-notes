#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string) {
    size_t n = strlen(my_string);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) answer[i] = my_string[n - 1 - i];
    answer[n] = '\0';
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
// char* solution(const char* my_string) {  // 뒤집힌 문자열 풀이 시작
//     size_t n = strlen(my_string);  // n에 입력 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) answer[i] = my_string[n - 1 - i];  // 결과 앞쪽부터 원본의 뒤쪽 문자를 대칭 인덱스로 복사
//     answer[n] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 결과의 i번째 칸에 원본의 n - 1 - i번째 문자를 복사해 전체 순서를 반대로 만듦.
