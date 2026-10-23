#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int* solution(const char* s) {
    int* answer = calloc(2, sizeof(*answer));
    int length = (int)strlen(s), ones = 0;
    for (int i = 0; i < length; ++i) ones += s[i] == '1';
    while (length != 1 || ones != 1) {
        ++answer[0]; answer[1] += length - ones;
        int value = ones; length = 0; ones = 0;
        while (value) { ++length; ones += value & 1; value >>= 1; }
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// int* solution(const char* s) {  // 1의 개수를 세어 남은 길이를 구하고 그 길이를 이진수로 바꾸는 과정을 반복하기
//     int* answer = calloc(2, sizeof(*answer));  // 변환 횟수와 제거한 0 개수 공간 확보하고 0으로 시작
//     int length = (int)strlen(s), ones = 0;  // 현재 이진 표현 길이 / 현재 표현의 1 개수 저장
//     for (int i = 0; i < length; ++i) ones += s[i] == '1';  // 1인지 셀 문자 위치 순서대로 확인; 현재 표현의 1 개수 / 1인지 셀 문자 위치 더해 누적
//     while (length != 1 || ones != 1) {  // 문자열이 1이 될 때까지 0 제거와 길이의 이진 변환 반복
//         ++answer[0]; answer[1] += length - ones;  // 변환 횟수와 제거한 0 개수 갱신
//         int value = ones; length = 0; ones = 0;  // 다음 이진 표현을 만들 수 / 현재 이진 표현 길이 / 현재 표현의 1 개수 저장
//         while (value) { ++length; ones += value & 1; value >>= 1; }  // 다음 이진 표현을 만들 수가 남아 있으면 반복; 현재 이진 표현 길이 갱신
//     }  // 이 범위 끝
//     return answer;  // 변환 횟수와 제거한 0 개수 반환
// }  // 이 범위 끝

// 풀이 요약
// 1의 개수를 세어 남은 길이를 구하고 그 길이를 이진수로 바꾸는 과정을 반복하기
// 예: '110010101001'은 세 번 변환하며 0 여덟 개를 제거해 [3,8].; 초기 길이 N일 때 시간·공간 O(N)
