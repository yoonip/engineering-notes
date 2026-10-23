#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

char* solution(int food[], size_t food_len) {
    size_t half = 0; for (size_t i = 1; i < food_len; ++i) half += food[i] / 2;
    char* answer = malloc(half * 2 + 2); size_t out = 0;
    for (size_t i = 1; i < food_len; ++i) for (int j = 0; j < food[i] / 2; ++j) answer[out++] = '0' + (char)i;
    answer[half] = '0';
    for (size_t i = 0; i < half; ++i) answer[half + 1 + i] = answer[half - 1 - i];
    answer[half * 2 + 1] = '\0';
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
// char* solution(int food[], size_t food_len) {  // 각 음식의 절반 개수로 왼쪽 참가자의 순서를 만들기; 가운데 물 0과 왼쪽 순서의 역순을 이어 붙
//     size_t half = 0; for (size_t i = 1; i < food_len; ++i) half += food[i] / 2;  // 음식별 절반을 더해 한쪽 참가자가 먹을 총개수 계산
//     char* answer = malloc(half * 2 + 2); size_t out = 0;  // 물 가운데 두고 대칭으로 놓은 음식 순서 / 왼쪽 음식의 다음 위치 공간 확보
//     for (size_t i = 1; i < food_len; ++i) for (int j = 0; j < food[i] / 2; ++j) answer[out++] = '0' + (char)i;  // 음식 종류 번호 순서대로 확인; 같은 음식의 반복 횟수 / 왼쪽 음식의 다음 위치 갱신
//     answer[half] = '0';  // 물 가운데 두고 대칭으로 놓은 음식 순서 갱신
//     for (size_t i = 0; i < half; ++i) answer[half + 1 + i] = answer[half - 1 - i];  // 음식 종류 번호 순서대로 확인; 물 가운데 두고 대칭으로 놓은 음식 순서 갱신
//     answer[half * 2 + 1] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 물 가운데 두고 대칭으로 놓은 음식 순서 반환
// }  // 이 범위 끝

// 풀이 요약
// 각 음식의 절반 개수로 왼쪽 참가자의 순서를 만들기; 가운데 물 0과 왼쪽 순서의 역순을 이어 붙
