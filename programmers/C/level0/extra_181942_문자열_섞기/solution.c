#include <stdlib.h>
#include <string.h>

char* solution(const char* str1, const char* str2) {
    size_t n = strlen(str1);
    char* answer = malloc(2 * n + 1);
    for (size_t i = 0; i < n; ++i) { answer[2 * i] = str1[i]; answer[2 * i + 1] = str2[i]; }
    answer[2 * n] = '\0';
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <string.h>  // 문자열 길이·복사·비교 함수
//
// char* solution(const char* str1, const char* str2) {  // 문자열 섞기 풀이 시작
//     size_t n = strlen(str1);  // strlen으로 첫 문자열 길이를 구해 size_t형 n에 저장
//     char* answer = malloc(2 * n + 1);  // malloc으로 두 문자열을 섞은 결과와 종료 문자를 담을 공간을 할당
//     for (size_t i = 0; i < n; ++i) { answer[2 * i] = str1[i]; answer[2 * i + 1] = str2[i]; }  // for로 같은 인덱스를 순회하며 결과의 짝수 위치와 홀수 위치에 각각 문자를 넣기
//     answer[2 * n] = '\0';  // 문자열 끝에 널 문자를 넣어 혼합 결과를 종료
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝

// 풀이 요약
// 두 문자열에서 같은 위치의 문자를 번갈아 연결
