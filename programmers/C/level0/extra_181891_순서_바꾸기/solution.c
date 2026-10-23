#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int num_list[], size_t num_list_len, int n) {
    int* answer = malloc(num_list_len * sizeof(int));
    for (size_t i = 0; i < num_list_len; ++i) answer[i] = num_list[(i + n) % num_list_len];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int num_list[], size_t num_list_len, int n) {  // 순서 바꾸기 풀이 시작
//     int* answer = malloc(num_list_len * sizeof(int));  // answer를 저장할 메모리 확보
//     for (size_t i = 0; i < num_list_len; ++i) answer[i] = num_list[(i + n) % num_list_len];  // 원본의 n번째 인덱스부터 읽고 끝에 닿으면 처음으로 돌아가 배열 순서 회전
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 앞 n개와 나머지로 나누고 두 묶음의 순서를 바꾸기
