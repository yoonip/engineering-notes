#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

char* solution(int n) {
    char* answer = malloc(n * 3 + 1);
    for (int i = 0; i < n; ++i) memcpy(answer + i * 3, i % 2 == 0 ? "수" : "박", 3);
    answer[n * 3] = '\0';
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
// char* solution(int n) {  // 수와 박을 번갈아 붙여 n글자를 만들기; C에서는 한글 한 글자의 UTF-8 바이트 세 개를 함께 복사
//     char* answer = malloc(n * 3 + 1);  // 수박을 반복한 UTF-8 문자열 공간 확보
//     for (int i = 0; i < n; ++i) memcpy(answer + i * 3, i % 2 == 0 ? "수" : "박", 3);  // 수와 박을 고를 위치 순서대로 확인; 수박을 반복한 UTF-8 문자열 / 수와 박을 고를 위치 복사
//     answer[n * 3] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 수박을 반복한 UTF-8 문자열 반환
// }  // 이 범위 끝

// 풀이 요약
// 수와 박을 번갈아 붙여 n글자를 만들기; C에서는 한글 한 글자의 UTF-8 바이트 세 개를 함께 복사
