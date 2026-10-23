#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(int num_list[], size_t num_list_len, int n) {
    size_t length = num_list_len - n + 1;
    int* answer = malloc(length * sizeof(int));
    memcpy(answer, num_list + n - 1, length * sizeof(int));
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int* solution(int num_list[], size_t num_list_len, int n) {  // n 번째 원소부터 풀이 시작
//     size_t length = num_list_len - n + 1;  // 결과의 원소 수 저장
//     int* answer = malloc(length * sizeof(int));  // answer를 저장할 메모리 확보
//     memcpy(answer, num_list + n - 1, length * sizeof(int));  // 1기준 n번째 원소인 인덱스 n - 1부터 배열 끝까지 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 1부터 세는 순번과 0부터 세는 인덱스를 구분
