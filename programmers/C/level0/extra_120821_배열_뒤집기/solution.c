#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(int num_list[], size_t num_list_len) {
    int* answer = malloc(num_list_len * sizeof(*answer));
    for (size_t i = 0; i < num_list_len; ++i) answer[i] = num_list[num_list_len - 1 - i];
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int* solution(int num_list[], size_t num_list_len) {  // 배열 뒤집기 풀이 시작
//     int* answer = malloc(num_list_len * sizeof(*answer));  // malloc으로 원소 수만큼 int를 저장할 메모리를 할당하고 결과 배열의 주소를 answer에 저장
//     for (size_t i = 0; i < num_list_len; ++i) answer[i] = num_list[num_list_len - 1 - i];  // 앞에서부터 채울 결과 인덱스 i를 늘리며, 입력의 num_list_len - 1 - i 위치에 있는 원소를 answer[i]에 복사
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력과 같은 길이의 결과 배열을 만들기. 결과의 i번째 칸에 입력의 뒤에서 i번째 원소를 복사
