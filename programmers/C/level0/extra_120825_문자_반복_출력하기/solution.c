#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* my_string, int n) {
    size_t len = strlen(my_string), pos = 0;
    char* answer = malloc(len * n + 1);
    for (size_t i = 0; i < len; ++i)
        for (int j = 0; j < n; ++j) answer[pos++] = my_string[i];
    answer[pos] = '\0';
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
// char* solution(const char* my_string, int n) {  // 문자 반복 출력하기 풀이 시작
//     size_t len = strlen(my_string), pos = 0;  // len에 입력 문자열 길이 저장 · 다음 문자를 쓸 위치는 0부터 시작
//     char* answer = malloc(len * n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < len; ++i)  // 입력 문자열의 각 글자를 원래 순서대로 선택
//         for (int j = 0; j < n; ++j) answer[pos++] = my_string[i];  // 현재 문자를 n번 연속으로 결과에 넣기
//     answer[pos] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 문자열 전체가 아닌 각 글자를 n번씩 반복
