#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int arr1[], size_t arr1_len, int arr2[], size_t arr2_len) {
    if (arr1_len != arr2_len) return arr1_len > arr2_len ? 1 : -1;
    int sum1 = 0, sum2 = 0;
    for (size_t i = 0; i < arr1_len; ++i) { sum1 += arr1[i]; sum2 += arr2[i]; }
    return (sum1 > sum2) - (sum1 < sum2);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int arr1[], size_t arr1_len, int arr2[], size_t arr2_len) {  // 배열 비교하기 풀이 시작
//     if (arr1_len != arr2_len) return arr1_len > arr2_len ? 1 : -1;  // 길이가 다르면 삼항 연산자로 arr1이 더 길 때 1, 더 짧을 때 -1을 즉시 반환
//     int sum1 = 0, sum2 = 0;  // 길이가 같은 두 배열의 원소 합을 저장할 sum1과 sum2를 0으로 초기화
//     for (size_t i = 0; i < arr1_len; ++i) { sum1 += arr1[i]; sum2 += arr2[i]; }  // 인덱스 i로 같은 위치의 원소를 순회하며 각 배열의 합을 따로 누적
//     return (sum1 > sum2) - (sum1 < sum2);  // 비교식의 참은 1, 거짓은 0이므로 arr1의 합이 크면 1, 작으면 -1, 같으면 0을 반환
// }  // 블록 끝

// 풀이 요약
// 배열 길이를 먼저 비교하고, 길이가 같을 때만 각각의 원소 합을 계산해 비교. 두 비교 결과가 모두 같으면 0을 반환
