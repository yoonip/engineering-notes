#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

int** solution(int n) {
    int** answer = malloc(n * sizeof(int*));
    for (int i = 0; i < n; ++i) answer[i] = calloc(n, sizeof(int));
    int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int row = 0, col = 0, direction = 0;
    for (int value = 1; value <= n * n; ++value) {
        answer[row][col] = value;
        if (value == n * n) break;
        int nr = row + dr[direction], nc = col + dc[direction];
        if (nr < 0 || nr >= n || nc < 0 || nc >= n || answer[nr][nc]) direction = (direction + 1) % 4;
        row += dr[direction]; col += dc[direction];
    }
    return answer;
}

// 전체 코드 줄별 설명
// #include <stdio.h>  // scanf·printf 등 표준 입출력
// #include <stdlib.h>  // 메모리 할당·정수 변환·정렬 함수
// #include <stdbool.h>  // C에서 bool·true·false 사용
// #include <string.h>  // 문자열 길이·복사·비교 함수
// #include <ctype.h>  // 문자 검사와 대소문자 변환
//
// int** solution(int n) {  // 정수를 나선형으로 배치하기 풀이 시작
//     int** answer = malloc(n * sizeof(int*));  // n개 행의 시작 주소를 담을 포인터 배열을 할당
//     for (int i = 0; i < n; ++i) answer[i] = calloc(n, sizeof(int));  // 각 행을 calloc으로 할당하여 아직 방문하지 않은 모든 칸을 0으로 초기화
//     int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};  // 오른쪽·아래·왼쪽·위 순서의 행 이동량 dr과 열 이동량 dc를 정의
//     int row = 0, col = 0, direction = 0;  // 현재 칸을 왼쪽 위 (0, 0), 현재 방향을 오른쪽인 0으로 초기화
//     for (int value = 1; value <= n * n; ++value) {  // 쓸 값 value를 1부터 n²까지 하나씩 늘리며 격자를 채움
//         answer[row][col] = value;  // 현재 행 row와 열 col의 칸에 value를 기록
//         if (value == n * n) break;  // 마지막 값 n²를 썼다면 다음 칸으로 이동할 필요가 없으므로 반복문을 끝
//         int nr = row + dr[direction], nc = col + dc[direction];  // 현재 방향의 이동량을 더해 직진했을 때의 다음 행 nr과 열 nc를 계산
//         if (nr < 0 || nr >= n || nc < 0 || nc >= n || answer[nr][nc]) direction = (direction + 1) % 4;  // 다음 칸이 격자 밖이거나 이미 채워졌으면 방향 번호를 1 늘리고 % 4로 시계 방향 회전
//         row += dr[direction]; col += dc[direction];  // 확정된 방향의 이동량을 현재 행과 열에 더해 다음에 채울 칸으로 이동
//     }  // 블록 끝
//     return answer;  // 완성한 결과 반환
// }  // 블록 끝
// 풀이 요약
// 0으로 초기화한 격자의 왼쪽 위에서 오른쪽으로 시작. 숫자를 하나씩 쓰고, 다음 칸이 격자 밖이거나 이미 채워졌으면 오른쪽·아래·왼쪽·위 순서로 방향을 바꾸어 이동
