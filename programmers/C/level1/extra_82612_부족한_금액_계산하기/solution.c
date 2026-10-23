#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

long long solution(int price, int money, int count) {
    long long needed = 1LL * price * count * (count + 1) / 2 - money;
    return needed > 0 ? needed : 0;
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
// long long solution(int price, int money, int count) {  // 등차수열의 합으로 전체 이용료를 구하고 현재 금액을 빼기; 중간 곱셈부터 long long을 사용
//     long long needed = 1LL * price * count * (count + 1) / 2 - money;  // 등차수열 이용료 합에서 가진 돈을 뺀 값 저장
//     return needed > 0 ? needed : 0;  // 등차수열 이용료 합에서 가진 돈을 뺀 값로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// 등차수열의 합으로 전체 이용료를 구하고 현재 금액을 빼기; 중간 곱셈부터 long long을 사용
