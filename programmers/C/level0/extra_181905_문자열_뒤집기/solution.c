#include <stdlib.h>
#include <string.h>

char* solution(const char* my_string, int s, int e) {
    char* answer = malloc(strlen(my_string) + 1);
    strcpy(answer, my_string);
    while (s < e) {
        char temp = answer[s];
        answer[s++] = answer[e];
        answer[e--] = temp;
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* my_string, int s, int e) {  // 문자열 뒤집기 풀이 시작
//     char* answer = malloc(strlen(my_string) + 1);  // malloc으로 결과 문자열과 마지막 널 문자를 저장할 공간을 동적으로 할당
//     strcpy(answer, my_string);  // strcpy로 종료 문자를 포함한 원본 문자열을 복사
//     while (s < e) {  // while로 양 끝 인덱스가 만날 때까지 문자 교환을 반복
//         char temp = answer[s];  // 두 문자를 교환할 때 덮어쓰지 않도록 왼쪽 문자를 임시 변수에 저장
//         answer[s++] = answer[e];  // 오른쪽 문자를 왼쪽에 대입한 뒤 후위 ++로 왼쪽 인덱스를 늘림
//         answer[e--] = temp;  // 임시 문자를 오른쪽에 대입한 뒤 후위 --로 오른쪽 인덱스를 줄이기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 양 끝을 포함한 s부터 e 구간만 뒤집기
