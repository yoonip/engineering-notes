#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* strArr[], size_t strArr_len) {
    int counts[31] = {0}, answer = 0;
    for (size_t i = 0; i < strArr_len; ++i) {
        int count = ++counts[strlen(strArr[i])];
        if (count > answer) answer = count;
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
// int solution(const char* strArr[], size_t strArr_len) {  // 문자열 묶기 풀이 시작
//     int counts[31] = {0}, answer = 0;  // 길이별 문자열 수 counts와 가장 큰 그룹 크기 answer를 0으로 초기화
//     for (size_t i = 0; i < strArr_len; ++i) {  // 각 문자열을 길이가 같은 그룹에 합류시킴
//         int count = ++counts[strlen(strArr[i])];  // 현재 문자열 길이의 빈도를 늘리고 증가한 그룹 크기 저장
//         if (count > answer) answer = count;  // 현재 그룹이 가장 크면 최대 그룹 크기 갱신
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 문자열의 내용이 아닌 길이를 기준으로 개수를 세고 최댓값을 구하기
