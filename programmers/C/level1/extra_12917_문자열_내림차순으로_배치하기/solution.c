#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

char* solution(const char* s) {
    int counts[128] = {0}; size_t n = strlen(s), out = 0;
    for (size_t i = 0; i < n; ++i) ++counts[(unsigned char)s[i]];
    char* answer = malloc(n + 1);
    for (int c = 127; c >= 0; --c) for (int i = 0; i < counts[c]; ++i) answer[out++] = (char)c;
    answer[n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// char* solution(const char* s) {  // 알파벳 문자를 문자 코드의 내림차순으로 배치하기
//     int counts[128] = {0}; size_t n = strlen(s), out = 0;  // 문자 코드별 등장 횟수 / 전체 글자 수 / 내림차순 결과의 다음 위치 저장
//     for (size_t i = 0; i < n; ++i) ++counts[(unsigned char)s[i]];  // i 순서대로 확인; 문자 코드별 등장 횟수 갱신
//     char* answer = malloc(n + 1);  // 내림차순 문자열 공간 확보
//     for (int c = 127; c >= 0; --c) for (int i = 0; i < counts[c]; ++i) answer[out++] = (char)c;  // 현재 꺼낼 문자 코드 순서대로 확인; 내림차순 결과의 다음 위치 갱신
//     answer[n] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 내림차순 문자열 반환
// }  // 이 범위 끝

// 풀이 요약
// 알파벳 문자를 문자 코드의 내림차순으로 배치하기
