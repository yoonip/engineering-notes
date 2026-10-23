#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int absolutes[], size_t absolutes_len, bool signs[], size_t signs_len) {
    int answer = 0;
    for (size_t i = 0; i < absolutes_len; ++i) answer += signs[i] ? absolutes[i] : -absolutes[i];
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
// int solution(int absolutes[], size_t absolutes_len, bool signs[], size_t signs_len) {  // 부호 배열이 참이면 절댓값을 더하고 거짓이면 빼기
//     int answer = 0;  // 부호를 적용한 정수 합 저장
//     for (size_t i = 0; i < absolutes_len; ++i) answer += signs[i] ? absolutes[i] : -absolutes[i];  // 부호와 절댓값을 함께 읽을 위치 순서대로 확인; 부호를 적용한 정수 합 / 부호와 절댓값을 함께 읽을 위치 더해 누적
//     return answer;  // 부호를 적용한 정수 합 반환
// }  // 이 범위 끝

// 풀이 요약
// 부호 배열이 참이면 절댓값을 더하고 거짓이면 빼기
