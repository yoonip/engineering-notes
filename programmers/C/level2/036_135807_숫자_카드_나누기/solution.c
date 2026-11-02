#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static int gcd(int a, int b) { while (b) { int r = a % b; a = b; b = r; } return a; }
int solution(int arrayA[], size_t arrayA_len, int arrayB[], size_t arrayB_len) {
    int a = 0, b = 0;
    for (size_t i = 0; i < arrayA_len; ++i) a = gcd(a, arrayA[i]);
    for (size_t i = 0; i < arrayB_len; ++i) b = gcd(b, arrayB[i]);
    int candidate_a = a, candidate_b = b;
    for (size_t i = 0; i < arrayB_len; ++i) if (arrayB[i] % a == 0) candidate_a = 0;
    for (size_t i = 0; i < arrayA_len; ++i) if (arrayA[i] % b == 0) candidate_b = 0;
    return candidate_a > candidate_b ? candidate_a : candidate_b;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // sqrtl 등 실수 수학 함수의 선언
//
// static int gcd(int a, int b) { while (b) { int r = a % b; a = b; b = r; } return a; }  // 나머지를 반복해서 최대공약수 구하기
// int solution(int arrayA[], size_t arrayA_len, int arrayB[], size_t arrayB_len) {  // 한쪽 카드 전체를 나누는 최대 후보는 최대공약수입니다. 그 값이 반대쪽 카드 하나를 나누면 그 약수들도 같은 카드를 나누므로 후보가 될 수 없습니다.
//     int a = 0, b = 0;  // A 전체의 최대공약수 / B 전체의 최대공약수 저장
//     for (size_t i = 0; i < arrayA_len; ++i) a = gcd(a, arrayA[i]);  // 다른 배열의 나눗셈 검사 위치 순서대로 확인; A 전체의 최대공약수 갱신
//     for (size_t i = 0; i < arrayB_len; ++i) b = gcd(b, arrayB[i]);  // 다른 배열의 나눗셈 검사 위치 순서대로 확인; B 전체의 최대공약수 갱신
//     int candidate_a = a, candidate_b = b;  // A를 모두 나누고 B는 못 나눌 후보 / B를 모두 나누고 A는 못 나눌 후보 저장
//     for (size_t i = 0; i < arrayB_len; ++i) if (arrayB[i] % a == 0) candidate_a = 0;  // B의 원소 하나라도 A의 최대공약수로 나뉘면 A 후보 탈락
//     for (size_t i = 0; i < arrayA_len; ++i) if (arrayA[i] % b == 0) candidate_b = 0;  // A의 원소 하나라도 B의 최대공약수로 나뉘면 B 후보 탈락
//     return candidate_a > candidate_b ? candidate_a : candidate_b;  // A를 모두 나누고 B는 못 나눌 후보 / B를 모두 나누고 A는 못 나눌 후보로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 한쪽 카드 전체를 나누는 최대 후보는 최대공약수입니다. 그 값이 반대쪽 카드 하나를 나누면 그 약수들도 같은 카드를 나누므로 후보가 될 수 없습니다.
// 예: A=[14,35,119], B=[18,30,102]에서는 A의 최대공약수 7이 B의 어떤 수도 나누지 않으므로 답은 7입니다. 카드 N개·최댓값 V에 대해 시간은 O(N log V), 추가 공간은 O(1)입니다.
