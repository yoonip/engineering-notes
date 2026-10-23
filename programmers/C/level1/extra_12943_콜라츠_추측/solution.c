#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int num) {
    long long value = num; int count = 0;
    while (value != 1 && count < 500) { value = value % 2 ? value * 3 + 1 : value / 2; ++count; }
    return value == 1 ? count : -1;
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
// int solution(int num) {  // 짝수면 2로 나누고 홀수면 3배한 뒤 1을 더하기; 500번 안에 1이 되지 않으면 -1을 반환
//     long long value = num; int count = 0;  // 콜라츠 연산 중인 수 / 지금까지 적용한 연산 횟수 저장
//     while (value != 1 && count < 500) { value = value % 2 ? value * 3 + 1 : value / 2; ++count; }  // 1이 되거나 500회를 채울 때까지 홀수는 3배 더하기 1, 짝수는 절반으로 바꾸기
//     return value == 1 ? count : -1;  // 콜라츠 연산 중인 수 / 지금까지 적용한 연산 횟수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 짝수면 2로 나누고 홀수면 3배한 뒤 1을 더하기; 500번 안에 1이 되지 않으면 -1을 반환
