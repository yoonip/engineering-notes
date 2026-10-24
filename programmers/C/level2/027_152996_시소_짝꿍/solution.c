#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

long long solution(int weights[], size_t weights_len) {
    long long counts[2001] = {0}, answer = 0;
    for (size_t i = 0; i < weights_len; ++i) ++counts[weights[i]];
    for (int value = 100; value <= 1000; ++value) {
        answer += counts[value] * (counts[value] - 1) / 2;
        answer += counts[value] * counts[value * 2];
        if (value % 2 == 0) answer += counts[value] * counts[value * 3 / 2];
        if (value % 3 == 0) answer += counts[value] * counts[value * 4 / 3];
    }
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
// long long solution(int weights[], size_t weights_len) {  // 균형 가능한 무게 비는 1:1, 1:2, 2:3, 3:4; 같은 무게는 조합, 다른 무게는 인원 수의 곱으로 세기
//     long long counts[2001] = {0}, answer = 0;  // 몸무게별 사람 수 / 평형을 이루는 사람 쌍 수 저장
//     for (size_t i = 0; i < weights_len; ++i) ++counts[weights[i]];  // 입력 사람 위치 순서대로 확인; 몸무게별 사람 수 갱신
//     for (int value = 100; value <= 1000; ++value) {  // 가벼운 쪽 몸무게 순서대로 확인
//         answer += counts[value] * (counts[value] - 1) / 2;  // 평형을 이루는 사람 쌍 수 / 몸무게별 사람 수 / 가벼운 쪽 몸무게 더해 누적
//         answer += counts[value] * counts[value * 2];  // 평형을 이루는 사람 쌍 수 / 몸무게별 사람 수 / 가벼운 쪽 몸무게 더해 누적
//         if (value % 2 == 0) answer += counts[value] * counts[value * 3 / 2];  // 몸무게가 짝수일 때 2 대 3 비율의 상대 몸무게와 쌍 만들기
//         if (value % 3 == 0) answer += counts[value] * counts[value * 4 / 3];  // 몸무게가 3의 배수일 때 3 대 4 비율의 상대 몸무게와 쌍 만들기
//     }  // 이 범위 끝
//     return answer;  // 평형을 이루는 사람 쌍 수 반환
// }  // 이 범위 끝

// 풀이 요약
// 균형 가능한 무게 비는 1:1, 1:2, 2:3, 3:4; 같은 무게는 조합, 다른 무게는 인원 수의 곱으로 세기
// 예: [100,180,360,100,270]은 4쌍; 더 무거운 상대만 세어 중복 방지; 사람 N명·서로 다른 무게 U개일 때 시간 O(N+U), 공간 O(U)
