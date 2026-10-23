#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(int array[], size_t array_len) {
    int count = 0;
    for (size_t i = 0; i < array_len; ++i)
        for (int n = array[i]; n; n /= 10) count += n % 10 == 7;
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(int array[], size_t array_len) {  // 7의 개수 풀이 시작
//     int count = 0;  // 숫자 7을 발견한 횟수를 누적할 count를 0으로 초기화
//     for (size_t i = 0; i < array_len; ++i)  // 자릿수를 검사할 정수의 인덱스 i를 배열 전체에 대해 순회
//         for (int n = array[i]; n; n /= 10) count += n % 10 == 7;  // 현재 수 n의 일의 자리가 7이면 1을 더하고, 정수 나눗셈 n /= 10으로 다음 자릿수를 검사
//     return count;  // 배열의 모든 정수에서 발견한 자릿수 7의 총개수를 반환
// }  // 블록 끝
// 풀이 요약
// 각 수에서 n % 10으로 끝자리가 7인지 확인하고 n /= 10으로 제거. 모든 자릿수에서 발견한 7의 개수 합산.
