#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int num_list[], size_t num_list_len, int n) {
    int* answer = malloc(n * sizeof(int));
    memcpy(answer, num_list, n * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int num_list[], size_t num_list_len, int n) {  // n 번째 원소까지 풀이 시작
//     int* answer = malloc(n * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, num_list, n * sizeof(int));  // 입력 배열의 앞 n개 원소를 새 결과 배열에 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 원본 배열의 앞 n개 원소를 새 배열에 복사.
