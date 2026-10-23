#include <stdlib.h>

int* solution(const char* my_string) {
    int* answer = calloc(52, sizeof(int));
    for (const char* p = my_string; *p; ++p) {
        int index = *p >= 'A' && *p <= 'Z' ? *p - 'A' : *p - 'a' + 26;
        ++answer[index];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
//
// int* solution(const char* my_string) {  // 문자 개수 세기 풀이 시작
//     int* answer = calloc(52, sizeof(int));  // calloc으로 52개 정수의 저장 공간을 만들고 모두 0으로 초기화
//     for (const char* p = my_string; *p; ++p) {  // const 문자 포인터를 for로 이동하며 널 문자 직전까지 순회
//         int index = *p >= 'A' && *p <= 'Z' ? *p - 'A' : *p - 'a' + 26;  // *로 현재 문자를 읽고 삼항 연산자로 대소문자를 나누어 개수 배열의 인덱스로 바꾸기
//         ++answer[index];  // []로 해당 알파벳의 개수를 찾아 ++로 1을 더하기
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 대문자 26개와 소문자 26개에 서로 다른 인덱스를 배정해 개수를 세기
