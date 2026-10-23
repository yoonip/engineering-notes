#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

double solution(int numbers[], size_t numbers_len) {
    double sum = 0;
    for (size_t i = 0; i < numbers_len; ++i) sum += numbers[i];
    return sum / numbers_len;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// double solution(int numbers[], size_t numbers_len) {  // 배열의 평균값 풀이 시작
//     double sum = 0;  // 평균을 구할 합. 소수 부분을 남기려고 double 사용
//     for (size_t i = 0; i < numbers_len; ++i) sum += numbers[i];  // 배열의 모든 원소를 double 합에 더함
//     return sum / numbers_len;  // 실수 합을 원소 수로 나눠 평균 반환
// }  // 블록 끝
// 풀이 요약
// 평균은 전체 합을 원소 개수로 나눈 값임
