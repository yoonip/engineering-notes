#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int num_list[], size_t num_list_len, int n) {
    for (size_t i = 0; i < num_list_len; ++i) if (num_list[i] == n) return 1;
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int num_list[], size_t num_list_len, int n) {  // 정수 찾기 풀이 시작
//     for (size_t i = 0; i < num_list_len; ++i) if (num_list[i] == n) return 1;  // 배열에서 n과 같은 원소를 처음 찾으면 1 반환
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝
// 풀이 요약
// 배열을 앞에서부터 순회해 정수 n과 같은 원소가 하나라도 있는지 확인.
