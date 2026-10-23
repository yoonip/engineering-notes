#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static long long integer_sqrt(long long value) {
    long long root = (long long)sqrtl((long double)value);
    while ((root + 1) * (root + 1) <= value) ++root;
    while (root * root > value) --root;
    return root;
}
long long solution(int r1, int r2) {
    long long answer = 0;
    for (long long x = 1; x <= r2; ++x) {
        long long high = integer_sqrt((long long)r2 * r2 - x * x), inner = (long long)r1 * r1 - x * x;
        if (inner < 0) inner = 0;
        long long low = integer_sqrt(inner); if (low * low < inner) ++low;
        answer += high - low + 1;
    }
    return 4 * answer;
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
// static long long integer_sqrt(long long value) {  // 제곱근 근삿값을 정수 비교로 보정
//     long long root = (long long)sqrtl((long double)value);  // 정수 제곱근 후보 저장
//     while ((root + 1) * (root + 1) <= value) ++root;  // 다음 정수의 제곱도 value 이하인 동안 근삿값 올리기
//     while (root * root > value) --root;  // 현재 제곱이 value를 넘는 동안 근삿값 내리기
//     return root;  // 정수 제곱근 후보 반환
// }  // 이 범위 끝
// long long solution(int r1, int r2) {  // x를 고정해 두 원 사이에 놓이는 정수 y의 최솟값·최댓값을 정수 제곱근으로 계산; 경계도 포함하기
//     long long answer = 0;  // 한 사분면에서 센 격자점 수 저장
//     for (long long x = 1; x <= r2; ++x) {  // 양의 가로 좌표 순서대로 확인
//         long long high = integer_sqrt((long long)r2 * r2 - x * x), inner = (long long)r1 * r1 - x * x;  // 큰 원 안의 가장 높은 y / 작은 원의 남은 세로 제곱 길이 저장
//         if (inner < 0) inner = 0;  // 작은 원의 남은 세로 제곱 길이가 0보다 작으면 작은 원의 남은 세로 제곱 길이 갱신
//         long long low = integer_sqrt(inner); if (low * low < inner) ++low;  // 작은 원 바깥이 되는 최소 y 저장
//         answer += high - low + 1;  // 한 사분면에서 센 격자점 수 / 큰 원 안의 가장 높은 y / 작은 원 바깥이 되는 최소 y 더해 누적
//     }  // 이 범위 끝
//     return 4 * answer;  // 한 사분면에서 센 격자점 수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// x를 고정해 두 원 사이에 놓이는 정수 y의 최솟값·최댓값을 정수 제곱근으로 계산; 경계도 포함하기
// 예: r1=2,r2=3이면 한 영역 5개, 전체 20개.; x>0,y>=0을 세면 축도 중복 없이 네 배 됨; 시간 O(r2), 공간 O(1)
