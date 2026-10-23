#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int num_list[], size_t num_list_len) {
    int count = 0;
    for (size_t i = 0; i < num_list_len; ++i)
        for (int value = num_list[i]; value > 1; value /= 2) ++count;
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int num_list[], size_t num_list_len) {  // 1로 만들기 풀이 시작
//     int count = 0;  // 모든 원소를 1로 만드는 총 나눗셈 횟수 준비
//     for (size_t i = 0; i < num_list_len; ++i)  // 각 원소를 따로 1로 만드는 횟수 계산
//         for (int value = num_list[i]; value > 1; value /= 2) ++count;  // 각 수를 2로 나눠 1이 될 때까지의 연산 횟수 세기
//     return count;  // 각 원소에서 센 나눗셈 횟수의 합 반환
// }  // 블록 끝
// 풀이 요약
// 짝수는 절반, 홀수는 1을 뺀 뒤 절반으로 만드는 두 규칙 모두 양의 정수 나눗셈 / 2와 같음. 각 원소가 1이 될 때까지 나눈 횟수를 합산.
