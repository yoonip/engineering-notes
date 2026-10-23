#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int* solution(const char* myString) {
    size_t length = 1;
    for (size_t i = 0; myString[i]; ++i) if (myString[i] == 'x') ++length;
    int* answer = calloc(length, sizeof(int));
    size_t out = 0;
    for (size_t i = 0; myString[i]; ++i) {
        if (myString[i] == 'x') ++out;
        else ++answer[out];
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
// int* solution(const char* myString) {  // x 사이의 개수 풀이 시작
//     size_t length = 1;  // x가 없을 때도 조각 하나가 있으므로 결과 길이를 1로 시작
//     for (size_t i = 0; myString[i]; ++i) if (myString[i] == 'x') ++length;  // x마다 구간이 하나 더 생기므로 결과 배열 길이 계산
//     int* answer = calloc(length, sizeof(int));  // answer에 쓸 메모리를 0으로 채워 확보
//     size_t out = 0;  // 현재 길이를 세는 문자열 조각 번호를 0으로 시작
//     for (size_t i = 0; myString[i]; ++i) {  // 문자열을 읽으며 x로 나뉜 각 구간의 길이 세기
//         if (myString[i] == 'x') ++out;  // x를 만나면 다음 문자열 조각으로 이동
//         else ++answer[out];  // x가 아닌 문자는 현재 조각 길이에 1 추가
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 연속된 x 사이와 양 끝의 빈 조각도 길이 0으로 기록
