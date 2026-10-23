#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

char* solution(const char* rsp) {
    size_t n = strlen(rsp);
    char* answer = malloc(n + 1);
    for (size_t i = 0; i < n; ++i) answer[i] = rsp[i] == '2' ? '0' : rsp[i] == '0' ? '5' : '2';
    answer[n] = '\0';
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
// char* solution(const char* rsp) {  // 가위 바위 보 풀이 시작
//     size_t n = strlen(rsp);  // n에 입력 문자열 길이 저장
//     char* answer = malloc(n + 1);  // answer를 저장할 메모리 확보. 문자열 끝의 \0 자리도 포함
//     for (size_t i = 0; i < n; ++i) answer[i] = rsp[i] == '2' ? '0' : rsp[i] == '0' ? '5' : '2';  // 각 상대 패를 이기는 패로 치환: 가위 2→바위 0, 바위 0→보 5, 보 5→가위 2
//     answer[n] = '\0';  // 문자열 끝에 널 문자 \0을 기록하여 문자열의 종료 위치를 표시
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 가위 2에는 바위 0, 바위 0에는 보 5, 보 5에는 가위 2를 대응시켜 모든 패를 이기는 문자열 생성.
