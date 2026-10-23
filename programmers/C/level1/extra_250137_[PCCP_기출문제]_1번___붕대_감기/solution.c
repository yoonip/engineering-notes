#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

int solution(int bandage[], size_t bandage_len, int health, int** attacks, size_t attacks_rows, size_t attacks_cols) {
    int current = health, previous = 0;
    for (size_t i = 0; i < attacks_rows; ++i) {
        int quiet = attacks[i][0] - previous - 1;
        current += quiet * bandage[1] + quiet / bandage[0] * bandage[2];
        if (current > health) current = health;
        current -= attacks[i][1];
        if (current <= 0) return -1;
        previous = attacks[i][0];
    }
    return current;
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
// int solution(int bandage[], size_t bandage_len, int health, int** attacks, size_t attacks_rows, size_t attacks_cols) {  // 연속된 두 공격 사이의 빈 시간으로 회복량과 연속 성공 보너스를 계산; 최대 체력을 넘지 않게 한 뒤 공격 피해를 적용하기
//     int current = health, previous = 0;  // 현재 체력 / 직전 공격 시각 저장
//     for (size_t i = 0; i < attacks_rows; ++i) {  // 처리할 공격 위치 순서대로 확인
//         int quiet = attacks[i][0] - previous - 1;  // 이번 공격 전 회복 가능한 초 수 저장
//         current += quiet * bandage[1] + quiet / bandage[0] * bandage[2];  // 현재 체력 / 이번 공격 전 회복 가능한 초 수 더해 누적
//         if (current > health) current = health;  // 회복 후 체력이 최대 체력을 넘지 않도록 제한
//         current -= attacks[i][1];  // 현재 체력 / 처리할 공격 위치에서 이번 사용량 빼기
//         if (current <= 0) return -1;  // 현재 체력가 0 이하이면 조건에 맞는 답이 없으면 -1
//         previous = attacks[i][0];  // 직전 공격 시각 갱신
//     }  // 이 범위 끝
//     return current;  // 현재 체력 반환
// }  // 이 범위 끝

// 풀이 요약
// 연속된 두 공격 사이의 빈 시간으로 회복량과 연속 성공 보너스를 계산; 최대 체력을 넘지 않게 한 뒤 공격 피해를 적용하기
