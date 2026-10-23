#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int arr[], size_t arr_len) {
    size_t length = 0;
    for (size_t i = 0; i < arr_len; ++i) length += arr[i];
    int* answer = malloc(length * sizeof(int));
    size_t out = 0;
    for (size_t i = 0; i < arr_len; ++i) for (int j = 0; j < arr[i]; ++j) answer[out++] = arr[i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int arr[], size_t arr_len) {  // 배열의 원소만큼 추가하기 풀이 시작
//     size_t length = 0;  // 결과의 원소 수 저장
//     for (size_t i = 0; i < arr_len; ++i) length += arr[i];  // 각 값만큼 반복할 총 원소 수를 합산해 결과 길이 계산
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     size_t out = 0;  // 다음 결과를 기록할 위치 저장
//     for (size_t i = 0; i < arr_len; ++i) for (int j = 0; j < arr[i]; ++j) answer[out++] = arr[i];  // 각 원소의 값만큼 그 원소를 반복해 결과에 넣기
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 각 수 a를 a번 반복한 묶음을 입력 순서대로 연결
