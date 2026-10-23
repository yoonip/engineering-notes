#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    size_t length = 1;
    while (length < arr_len) length *= 2;
    int* answer = calloc(length, sizeof(int));
    memcpy(answer, arr, arr_len * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 배열의 길이를 2의 거듭제곱으로 만들기 풀이 시작
//     size_t length = 1;  // 반환 배열의 길이 후보 length를 가장 작은 2의 거듭제곱인 1로 초기화
//     while (length < arr_len) length *= 2;  // length가 원래 길이보다 작을 동안 두 배로 늘려 필요한 최소 길이를 찾기
//     int* answer = calloc(length, sizeof(int));  // calloc으로 length개의 int 공간을 할당하고 모든 원소를 0으로 초기화
//     memcpy(answer, arr, arr_len * sizeof(int));  // memcpy로 원래 원소 arr_len개를 앞부분에 복사하여 추가된 뒷부분의 0을 유지
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 1부터 두 배씩 늘려 원래 배열 길이 이상인 가장 작은 2의 거듭제곱을 찾기. 해당 길이의 배열을 0으로 초기화한 뒤 원래 원소만 앞부분에 복사
