#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* myString, const char* pat) {
    size_t n = strlen(myString), m = strlen(pat);
    if (m > n) return 0;
    for (size_t i = 0; i + m <= n; ++i) {
        size_t j = 0;
        while (j < m && (myString[i + j] == 'A' ? 'B' : 'A') == pat[j]) ++j;
        if (j == m) return 1;
    }
    return 0;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* myString, const char* pat) {  // 문자열 바꿔서 찾기 풀이 시작
//     size_t n = strlen(myString), m = strlen(pat);  // 원본 길이 n과 패턴 길이 m 저장
//     if (m > n) return 0;  // 패턴이 더 길면 어느 시작점에서도 맞을 수 없어 0 반환
//     for (size_t i = 0; i + m <= n; ++i) {  // 패턴을 끝까지 비교할 수 있는 시작 위치 순회
//         size_t j = 0;  // 현재 시작점에서 일치한 패턴 길이를 0으로 초기화
//         while (j < m && (myString[i + j] == 'A' ? 'B' : 'A') == pat[j]) ++j;  // 원본 A는 B로, B는 A로 바꾼 값과 패턴을 비교하며 일치 길이 증가
//         if (j == m) return 1;  // 변환한 문자들이 패턴 전체와 일치하면 1 반환
//     }  // 블록 끝
//     return 0;  // 조건에 맞는 경우가 없으면 0 반환
// }  // 블록 끝
// 풀이 요약
// 각 시작 위치에서 A는 B로, B는 A로 바꾼 문자를 pat과 직접 비교. 변환된 문자열을 따로 만들지 않고 패턴 전체가 맞는지 검사.
