#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

char* solution(const char* phone_number) {
    size_t n = strlen(phone_number); char* answer = malloc(n + 1); strcpy(answer, phone_number);
    for (size_t i = 0; i + 4 < n; ++i) answer[i] = '*';
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
// char* solution(const char* phone_number) {  // 문자열의 마지막 네 자리를 제외한 모든 문자를 별표로 바꾸기
//     size_t n = strlen(phone_number); char* answer = malloc(n + 1); strcpy(answer, phone_number);  // 전화번호 길이 / 뒤 네 자리만 남긴 전화번호 공간 확보
//     for (size_t i = 0; i + 4 < n; ++i) answer[i] = '*';  // 별표로 가릴 앞부분 위치 순서대로 확인; 뒤 네 자리만 남긴 전화번호 갱신
//     return answer;  // 뒤 네 자리만 남긴 전화번호 반환
// }  // 이 범위 끝

// 풀이 요약
// 문자열의 마지막 네 자리를 제외한 모든 문자를 별표로 바꾸기
