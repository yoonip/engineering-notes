#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

double solution(int arr[], size_t arr_len) {
    long long sum = 0; for (size_t i = 0; i < arr_len; ++i) sum += arr[i];
    return (double)sum / arr_len;
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
// double solution(int arr[], size_t arr_len) {  // 모든 원소의 합을 실수로 바꾸어 원소 수로 나누기
//     long long sum = 0; for (size_t i = 0; i < arr_len; ++i) sum += arr[i];  // 배열 원소의 합 / 평균에 더할 원소 위치 저장
//     return (double)sum / arr_len;  // 배열 원소의 합로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 모든 원소의 합을 실수로 바꾸어 원소 수로 나누기
