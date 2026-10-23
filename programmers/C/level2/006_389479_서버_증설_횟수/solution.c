#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

int solution(int players[], size_t players_len, int m, int k) {
    int* expires = calloc(players_len + k, sizeof(*expires)); int active = 0, answer = 0;
    for (size_t hour = 0; hour < players_len; ++hour) {
        active -= expires[hour]; int added = players[hour] / m - active;
        if (added < 0) added = 0;
        active += added; answer += added; expires[hour + k] += added;
    }
    free(expires);
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
// int solution(int players[], size_t players_len, int m, int k) {  // 매 시간 만료 서버를 먼저 빼고, 필요한 서버 수 people//m에서 부족한 만큼만 증설하기
//     int* expires = calloc(players_len + k, sizeof(*expires)); int active = 0, answer = 0;  // 시각별 반납할 서버 수 / 현재 돌아가는 증설 서버 수 / 서버를 증설한 총대수 공간 확보하고 0으로 시작
//     for (size_t hour = 0; hour < players_len; ++hour) {  // 현재 시간대 순서대로 확인
//         active -= expires[hour]; int added = players[hour] / m - active;  // 현재 돌아가는 증설 서버 수 / 시각별 반납할 서버 수 / 현재 시간대에서 이번 사용량 빼기
//         if (added < 0) added = 0;  // 이번 시간에 더 필요한 서버가 0보다 작으면 이번 시간에 더 필요한 서버 갱신
//         active += added; answer += added; expires[hour + k] += added;  // 현재 돌아가는 증설 서버 수 / 이번 시간에 더 필요한 서버 / 서버를 증설한 총대수 더해 누적
//     }  // 이 범위 끝
//     free(expires);  // 시각별 반납할 서버 수 임시 공간 정리
//     return answer;  // 서버를 증설한 총대수 반환
// }  // 이 범위 끝

// 풀이 요약
// 매 시간 만료 서버를 먼저 빼고, 필요한 서버 수 people//m에서 부족한 만큼만 증설하기
// 새 서버는 hour+k에 만료됨; 시간·공간 O(시간 수+k)
// 예: m=3, 현재 2대, 이용자 10명이면 10//3=3대가 필요하므로 1대를 추가하기
