#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int num_list[], size_t num_list_len) {
    int result = num_list_len >= 11 ? 0 : 1;
    for (size_t i = 0; i < num_list_len; ++i) {
        if (num_list_len >= 11) result += num_list[i];
        else result *= num_list[i];
    }
    return result;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int num_list[], size_t num_list_len) {  // 길이에 따른 연산 풀이 시작
//     int result = num_list_len >= 11 ? 0 : 1;  // 배열 길이가 11 이상이면 합의 시작값 0, 그 외에는 곱의 시작값 1 선택
//     for (size_t i = 0; i < num_list_len; ++i) {  // 선택한 합 또는 곱 연산에 모든 원소 반영
//         if (num_list_len >= 11) result += num_list[i];  // 길이가 11 이상이면 현재 원소를 합산
//         else result *= num_list[i];  // 길이가 10 이하이면 현재 원소를 누적 곱에 곱함
//     }  // 블록 끝
//     return result;  // 배열 길이에 맞춰 계산한 합 또는 곱 반환
// }  // 블록 끝// 풀이 요약
// 길이에 따라 합계 또는 곱을 선택
