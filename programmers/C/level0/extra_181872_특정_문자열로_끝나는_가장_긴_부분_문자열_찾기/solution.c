#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

char* solution(const char* myString, const char* pat) {
    const char* last = myString;
    const char* found = strstr(myString, pat);
    while (found) { last = found; found = strstr(found + 1, pat); }
    size_t n = last - myString + strlen(pat);
    char* answer = malloc(n + 1);
    memcpy(answer, myString, n);
    answer[n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// char* solution(const char* myString, const char* pat) {  // 특정 문자열로 끝나는 가장 긴 부분 문자열 찾기 풀이 시작
//     const char* last = myString;  // pat의 마지막 등장 위치를 기록할 포인터 준비
//     const char* found = strstr(myString, pat);  // 패턴을 발견한 위치 저장
//     while (found) { last = found; found = strstr(found + 1, pat); }  // strstr로 다음 패턴 위치를 찾는 동안 반복하고 검색 시작 위치를 한 칸 옮기기
//     size_t n = last - myString + strlen(pat);  // 문자열 처음부터 마지막 pat의 끝까지 포함하는 길이 계산
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     memcpy(answer, myString, n);  // 마지막 pat의 끝까지 원본 앞부분을 결과에 복사
//     answer[n] = '\0';  // 문자열 끝에 널 종료 문자를 기록
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열임
