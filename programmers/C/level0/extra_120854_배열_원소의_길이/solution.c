#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(const char* strlist[], size_t strlist_len) {
    int* answer = malloc(strlist_len * sizeof(*answer));
    for (size_t i = 0; i < strlist_len; ++i) answer[i] = (int)strlen(strlist[i]);
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
// int* solution(const char* strlist[], size_t strlist_len) {  // 배열 원소의 길이 풀이 시작
//     int* answer = malloc(strlist_len * sizeof(*answer));  // malloc으로 문자열 개수만큼 int를 저장할 메모리를 할당하고, 그 주소를 answer 포인터에 저장. sizeof(*answer)는 int 한 개의 크기임
//     for (size_t i = 0; i < strlist_len; ++i) answer[i] = (int)strlen(strlist[i]);  // 인덱스 i로 모든 문자열을 순회하며 strlen이 센 문자 수를 int로 변환해 대응하는 answer[i]에 저장
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 입력 문자열과 같은 개수의 정수 칸을 마련하고, 각 문자열의 길이를 원래 순서대로 저장
