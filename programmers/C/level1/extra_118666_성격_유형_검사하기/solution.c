#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

char* solution(const char* survey[], size_t survey_len, int choices[], size_t choices_len) {
    int points[128] = {0};
    for (size_t i = 0; i < survey_len; ++i) {
        if (choices[i] < 4) points[(unsigned char)survey[i][0]] += 4 - choices[i];
        else if (choices[i] > 4) points[(unsigned char)survey[i][1]] += choices[i] - 4;
    }
    const char* pairs[4] = {"RT", "CF", "JM", "AN"}; char* answer = malloc(5);
    for (int i = 0; i < 4; ++i) answer[i] = points[(int)pairs[i][0]] >= points[(int)pairs[i][1]] ? pairs[i][0] : pairs[i][1];
    answer[4] = '\0';
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
// char* solution(const char* survey[], size_t survey_len, int choices[], size_t choices_len) {  // 선택지의 동의·비동의 정도를 각 성격 지표의 점수에 더하기; 점수가 같으면 사전순으로 앞선 지표를 선택
//     int points[128] = {0};  // 성격 문자별 누적 점수 저장
//     for (size_t i = 0; i < survey_len; ++i) {  // 설문 또는 성격 쌍 위치 순서대로 확인
//         if (choices[i] < 4) points[(unsigned char)survey[i][0]] += 4 - choices[i];  // 비동의 응답이면 첫 성격 문자에 4와의 차이만큼 점수 추가
//         else if (choices[i] > 4) points[(unsigned char)survey[i][1]] += choices[i] - 4;  // 동의 응답이면 둘째 성격 문자에 4와의 차이만큼 점수 추가
//     }  // 이 범위 끝
//     const char* pairs[4] = {"RT", "CF", "JM", "AN"}; char* answer = malloc(5);  // 동점 우선순서로 적은 성격 쌍 / 네 쌍에서 고른 성격 유형 공간 확보
//     for (int i = 0; i < 4; ++i) answer[i] = points[(int)pairs[i][0]] >= points[(int)pairs[i][1]] ? pairs[i][0] : pairs[i][1];  // 설문 또는 성격 쌍 위치 순서대로 확인; 네 쌍에서 고른 성격 유형 갱신
//     answer[4] = '\0';  // 문자열 끝에 널 문자 붙이기
//     return answer;  // 네 쌍에서 고른 성격 유형 반환
// }  // 이 범위 끝

// 풀이 요약
// 선택지의 동의·비동의 정도를 각 성격 지표의 점수에 더하기; 점수가 같으면 사전순으로 앞선 지표를 선택
