#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    int* answer = malloc(arr_len * sizeof(int));
    for (size_t i = 0; i < arr_len; ++i) {
        int x = arr[i];
        answer[i] = x >= 50 && x % 2 == 0 ? x / 2 : x < 50 && x % 2 ? x * 2 : x;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 조건에 맞게 수열 변환하기 1 풀이 시작
//     int* answer = malloc(arr_len * sizeof(int));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < arr_len; ++i) {  // 각 원소에 조건별 변환 규칙 적용
//         int x = arr[i];  // 이번에 규칙을 적용할 원소를 x에 보관
//         answer[i] = x >= 50 && x % 2 == 0 ? x / 2 : x < 50 && x % 2 ? x * 2 : x;  // 50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 원래 값 저장
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 그대로 두기
