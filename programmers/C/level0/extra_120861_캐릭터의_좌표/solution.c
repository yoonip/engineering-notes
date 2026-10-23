#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>

int* solution(const char* keyinput[], size_t keyinput_len, int board[], size_t board_len) {
    (void)board_len;
    int* answer = calloc(2, sizeof(*answer));
    for (size_t i = 0; i < keyinput_len; ++i) {
        int x = answer[0], y = answer[1];
        if (strcmp(keyinput[i], "left") == 0) --x;
        else if (strcmp(keyinput[i], "right") == 0) ++x;
        else if (strcmp(keyinput[i], "up") == 0) ++y;
        else --y;
        if (abs(x) <= board[0] / 2 && abs(y) <= board[1] / 2) {
            answer[0] = x; answer[1] = y;
        }
    }
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
// int* solution(const char* keyinput[], size_t keyinput_len, int board[], size_t board_len) {  // 캐릭터의 좌표 풀이 시작
//     (void)board_len;  // 배열 크기처럼 함수 형식에 포함되지만 본문에서 사용하지 않는 매개변수임을 표시
//     int* answer = calloc(2, sizeof(*answer));  // calloc은 지정한 개수의 메모리를 확보하고 모든 바이트를 0으로 초기화
//     for (size_t i = 0; i < keyinput_len; ++i) {  // 방향 명령을 순서대로 적용
//         int x = answer[0], y = answer[1];  // 실제 위치를 바꾸기 전에 다음 좌표를 x·y에 임시 계산
//         if (strcmp(keyinput[i], "left") == 0) --x;  // 왼쪽 명령이면 후보 x좌표를 1 감소
//         else if (strcmp(keyinput[i], "right") == 0) ++x;  // 오른쪽 명령이면 후보 x좌표를 1 증가
//         else if (strcmp(keyinput[i], "up") == 0) ++y;  // 위쪽 명령이면 후보 y좌표를 1 증가
//         else --y;  // 아래쪽 명령이면 후보 y좌표를 1 감소
//         if (abs(x) <= board[0] / 2 && abs(y) <= board[1] / 2) {  // 다음 좌표가 보드의 가로·세로 범위 안일 때만 이동 확정
//             answer[0] = x; answer[1] = y;  // 유효한 다음 좌표를 실제 위치에 반영
//         }  // 블록 끝
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 이동할 후보 좌표를 먼저 만들고 지도 경계 안에 있을 때만 반영
