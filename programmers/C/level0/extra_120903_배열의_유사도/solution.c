#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int solution(const char* s1[], size_t s1_len, const char* s2[], size_t s2_len) {
    int count = 0;
    for (size_t i = 0; i < s1_len; ++i)
        for (size_t j = 0; j < s2_len; ++j)
            if (strcmp(s1[i], s2[j]) == 0) { ++count; break; }
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <ctype.h>  // 문자 검사와 대소문자 변환
// #include <limits.h>  // 정수형 최솟값·최댓값 상수
//
// int solution(const char* s1[], size_t s1_len, const char* s2[], size_t s2_len) {  // 배열의 유사도 풀이 시작
//     int count = 0;  // 두 배열에 공통으로 들어 있는 문자열 수를 0으로 시작
//     for (size_t i = 0; i < s1_len; ++i)  // 첫 배열의 문자열을 하나씩 기준으로 선택
//         for (size_t j = 0; j < s2_len; ++j)  // 두 번째 배열에서 같은 문자열 탐색
//             if (strcmp(s1[i], s2[j]) == 0) { ++count; break; }  // 같은 문자열을 찾으면 공통 개수를 늘리고 현재 기준 문자열의 탐색 종료
//     return count;  // 두 배열에 공통으로 들어 있는 문자열 수 반환
// }  // 블록 끝// 풀이 요약
// 두 집합에 모두 포함된 원소의 개수를 구하기
