#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(int num_list[], size_t num_list_len) {
    for (size_t i = 0; i < num_list_len; ++i) if (num_list[i] < 0) return (int)i;
    return -1;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(int num_list[], size_t num_list_len) {  // 첫 번째로 나오는 음수 풀이 시작
//     for (size_t i = 0; i < num_list_len; ++i) if (num_list[i] < 0) return (int)i;  // 앞에서부터 검사해 처음 만난 음수의 인덱스 반환
//     return -1;  // 조건을 만족하는 위치가 없으므로 -1을 반환
// }  // 블록 끝
// 풀이 요약
// 앞에서부터 검사하면 처음 찾은 음수가 가장 먼저 등장한 음수임
