#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len, int k) {
    int* answer = malloc(arr_len * sizeof(int));
    for (size_t i = 0; i < arr_len; ++i) answer[i] = k % 2 ? arr[i] * k : arr[i] + k;
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len, int k) {  // 조건에 맞게 수열 변환하기 3 풀이 시작
//     int* answer = malloc(arr_len * sizeof(int));  // 입력 배열과 같은 개수의 int를 저장할 결과 공간을 malloc으로 할당
//     for (size_t i = 0; i < arr_len; ++i) answer[i] = k % 2 ? arr[i] * k : arr[i] + k;  // 각 원소를 순회하며 k % 2가 참이면 k를 곱하고, 거짓이면 k를 더한 값을 answer에 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 각 원소에 대해 k가 홀수이면 arr[i] * k를, 짝수이면 arr[i] + k를 계산하여 같은 위치의 새 배열에 저장
