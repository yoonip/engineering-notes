#include <stdio.h> // 격자와 명령의 표준 입력·출력
int main(void) { // 실행 시작점
    int h, w, row, col, direction, count; // 격자 크기와 로봇 상태
    char grid[10][11], command; // 최대 10칸 행과 명령 문자
    int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1}; // 북·동·남·서의 좌표 변화
    scanf("%d %d", &h, &w); // 격자 크기 입력
    for (int i = 0; i < h; ++i) scanf("%10s", grid[i]); // 점과 벽으로 된 행 읽기
    scanf("%d %d %d %d", &row, &col, &direction, &count); // 시작 좌표·방향·명령 수 입력
    for (int i = 0; i < count; ++i) { // 명령을 하나씩 순서대로 처리
        scanf(" %c", &command); // 앞 공백을 건너뛰고 명령 문자 읽기
        if (command == 'R') direction = (direction + 1) % 4; // 오른쪽 회전은 방향만 변경
        else { // F 명령의 다음 칸 검사
            int nr = row + dr[direction], nc = col + dc[direction]; // 아직 확정하지 않은 다음 좌표
            if (0 <= nr && nr < h && 0 <= nc && nc < w && grid[nr][nc] != '#') { // 범위와 벽을 함께 확인
                row = nr; col = nc; // 허용된 이동만 상태에 반영
            } // 이동 허용 검사 끝
        } // 전진 명령 처리 끝
    } // 모든 명령 처리 끝
    printf("%d %d %d\n", row, col, direction); // 최종 좌표와 방향 출력
    return 0; // 정상 종료
} // 로봇 시뮬레이션 끝
