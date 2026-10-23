#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

long long solution(int a, int b) {
    long long start = a < b ? a : b, end = a > b ? a : b;
    return (start + end) * (end - start + 1) / 2;
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
// long long solution(int a, int b) {  // 작은 수부터 큰 수까지의 등차수열 합을 계산; 중간 계산부터 long long을 사용
//     long long start = a < b ? a : b, end = a > b ? a : b;  // 두 수 중 작은 끝점 / 두 수 중 큰 끝점 저장
//     return (start + end) * (end - start + 1) / 2;  // 두 수 중 작은 끝점 / 두 수 중 큰 끝점로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 작은 수부터 큰 수까지의 등차수열 합을 계산; 중간 계산부터 long long을 사용
