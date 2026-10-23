#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <limits.h>

static int seconds_of(const char* time) {
    int minutes, seconds; sscanf(time, "%d:%d", &minutes, &seconds); return minutes * 60 + seconds;
}
char* solution(const char* video_len, const char* pos, const char* op_start, const char* op_end, const char* commands[], size_t commands_len) {
    int end = seconds_of(video_len), current = seconds_of(pos), opening = seconds_of(op_start), closing = seconds_of(op_end);
    if (opening <= current && current <= closing) current = closing;
    for (size_t i = 0; i < commands_len; ++i) {
        current += strcmp(commands[i], "prev") == 0 ? -10 : 10;
        if (current < 0) current = 0; if (current > end) current = end;
        if (opening <= current && current <= closing) current = closing;
    }
    char* answer = malloc(6); sprintf(answer, "%02d:%02d", current / 60, current % 60);
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
//
// static int seconds_of(const char* time) {  // 분:초 표기를 전체 초 수로 바꾸기
//     int minutes, seconds; sscanf(time, "%d:%d", &minutes, &seconds); return minutes * 60 + seconds;  // 분과 초를 읽어 전체 초 수로 환산
// }  // 이 범위 끝
// char* solution(const char* video_len, const char* pos, const char* op_start, const char* op_end, const char* commands[], size_t commands_len) {  // 현재 위치가 오프닝 구간이면 끝으로 건너뛰기; 각 명령마다 10초 이동과 영상 범위 제한을 적용한 뒤 오프닝을 다시 확인
//     int end = seconds_of(video_len), current = seconds_of(pos), opening = seconds_of(op_start), closing = seconds_of(op_end);  // 동영상 끝 시각 / 현재 재생 시각 / 오프닝 시작 / 오프닝 끝 저장
//     if (opening <= current && current <= closing) current = closing;  // 현재 시각이 오프닝 안이면 오프닝 끝으로 건너뛰기
//     for (size_t i = 0; i < commands_len; ++i) {  // 재생 명령 위치 순서대로 확인
//         current += strcmp(commands[i], "prev") == 0 ? -10 : 10;  // 현재 재생 시각 / 재생 명령 위치 더해 누적
//         if (current < 0) current = 0; if (current > end) current = end;  // 현재 재생 시각가 0보다 작으면 현재 재생 시각 갱신
//         if (opening <= current && current <= closing) current = closing;  // 현재 시각이 오프닝 안이면 오프닝 끝으로 건너뛰기
//     }  // 이 범위 끝
//     char* answer = malloc(6); sprintf(answer, "%02d:%02d", current / 60, current % 60);  // 분과 초로 바꾼 최종 시각 공간 확보
//     return answer;  // 분과 초로 바꾼 최종 시각 반환
// }  // 이 범위 끝

// 풀이 요약
// 현재 위치가 오프닝 구간이면 끝으로 건너뛰기; 각 명령마다 10초 이동과 영상 범위 제한을 적용한 뒤 오프닝을 다시 확인
