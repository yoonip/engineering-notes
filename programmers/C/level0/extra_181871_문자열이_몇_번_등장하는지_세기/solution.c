#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int solution(const char* myString, const char* pat) {
    int count = 0;
    const char* found = myString;
    while ((found = strstr(found, pat)) != NULL) { ++count; ++found; }
    return count;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int solution(const char* myString, const char* pat) {  // 문자열이 몇 번 등장하는지 세기 풀이 시작
//     int count = 0;  // pat의 등장 횟수를 0으로 시작
//     const char* found = myString;  // 패턴을 발견한 위치 저장
//     while ((found = strstr(found, pat)) != NULL) { ++count; ++found; }  // strstr로 다음 패턴 위치를 찾는 동안 반복하고 검색 시작 위치를 한 칸 옮기기
//     return count;  // 서로 겹치는 경우까지 포함한 pat의 전체 등장 횟수 반환
// }  // 블록 끝
// 풀이 요약
// 모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 세기
