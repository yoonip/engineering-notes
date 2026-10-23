#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

static bool wins(const char** board, char c) {
    for (int i = 0; i < 3; ++i)
        if ((board[i][0] == c && board[i][1] == c && board[i][2] == c) || (board[0][i] == c && board[1][i] == c && board[2][i] == c)) return true;
    return (board[0][0] == c && board[1][1] == c && board[2][2] == c) || (board[0][2] == c && board[1][1] == c && board[2][0] == c);
}
int solution(const char* board[], size_t board_len) {
    (void)board_len;
    int o = 0, x = 0;
    for (int r = 0; r < 3; ++r) for (int c = 0; c < 3; ++c) { o += board[r][c] == 'O'; x += board[r][c] == 'X'; }
    if (o != x && o != x + 1) return 0;
    bool o_win = wins(board, 'O'), x_win = wins(board, 'X');
    return !(o_win && x_win) && (!o_win || o == x + 1) && (!x_win || o == x);
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // 문자열 형식 읽기·쓰기용 표준 입출력 선언
// #include <stdlib.h>  // 동적 메모리, 정수 변환, 정렬 함수 선언
// #include <string.h>  // 문자열 길이·비교·복사와 메모리 함수 선언
// #include <stdbool.h>  // 참·거짓 표시용 bool, true, false
// #include <ctype.h>  // 문자 종류 확인과 대소문자 변환
// #include <limits.h>  // 최솟값·최댓값 초기화에 쓸 정수 범위 상수
// #include <math.h>  // 정수 제곱근 계산 등에 쓸 수학 함수
//
// static bool wins(const char** board, char c) {  // 가로·세로·대각선 세 칸이 같은지 확인
//     for (int i = 0; i < 3; ++i)  // 가로세로 승리 줄 번호 순서대로 확인
//         if ((board[i][0] == c && board[i][1] == c && board[i][2] == c) || (board[0][i] == c && board[1][i] == c && board[2][i] == c)) return true;  // 현재 가로줄이나 세로줄이 모두 같은 말이면 승리
//     return (board[0][0] == c && board[1][1] == c && board[2][2] == c) || (board[0][2] == c && board[1][1] == c && board[2][0] == c);  // 확인할 말 문자로 최종값 계산
// }  // 이 범위 끝
// int solution(const char* board[], size_t board_len) {  // O·X 개수로 차례를 검사하고, 승자가 있으면 그 승자의 마지막 차례에서 끝났는지 확인
//     (void)board_len;  // 입력 형식에만 필요한 길이 값은 계산에서 생략
//     int o = 0, x = 0;  // O를 둔 횟수 / X를 둔 횟수 저장
//     for (int r = 0; r < 3; ++r) for (int c = 0; c < 3; ++c) { o += board[r][c] == 'O'; x += board[r][c] == 'X'; }  // 보드 행 순서대로 확인; 확인할 말 문자 갱신
//     if (o != x && o != x + 1) return 0;  // O의 수가 X와 같거나 하나 더 많은 경우가 아니면 불가능
//     bool o_win = wins(board, 'O'), x_win = wins(board, 'X');  // O가 세 칸을 이었는지 여부 / X가 세 칸을 이었는지 여부 저장
//     return !(o_win && x_win) && (!o_win || o == x + 1) && (!x_win || o == x);  // O가 세 칸을 이었는지 여부 / X가 세 칸을 이었는지 여부 / O를 둔 횟수로 최종값 계산
// }  // 이 범위 끝

// 풀이 요약
// O·X 개수로 차례를 검사하고, 승자가 있으면 그 승자의 마지막 차례에서 끝났는지 확인
// 예: OOO와 XXX가 함께 있으면 0, 빈 판은 1.; 판이 항상 3×3이므로 시간·공간 O(1)
