#include <stdio.h>  // 표준 입력과 숫자·문자열 출력 함수
#include <stdlib.h>  // qsort와 정수 절댓값 함수
static int read_int(void) {  // 다음 정수 하나를 읽는 공통 함수
    int value = 0;  // 입력값을 받을 정수
    scanf("%d", &value);  // 공백을 건너뛰고 정수 읽기
    return value;  // 읽은 값 전달
}  // 정수 입력 함수 끝
static void read_word(char *text) {  // 길이가 32 이하인 토큰 입력
    scanf("%32s", text);  // 종료 문자까지 들어갈 33칸 버퍼 사용
}  // 토큰 입력 함수 끝
static void write_number(int value) {  // 정수 한 개를 출력하는 공통 함수
    printf("%d", value);  // 불필요한 공백 없이 정수 출력
}  // 정수 출력 함수 끝
static void write_text(const char *text) {  // 구분자나 결과 문구 출력
    fputs(text, stdout);  // 문자열을 표준 출력에 그대로 쓰기
}  // 문자열 출력 함수 끝


int main(void) {  // 최소 f 스캔 방식의 실제 A* 탐색
    int rows = read_int(), cols = read_int(), distance[25], closed[25] = {0};  // 격자 크기·최선 g·닫힌 상태
    char grid[5][33];  // 토큰 입력 함수의 최대 폭을 담는 행 버퍼
    for (int r = 0; r < rows; ++r) read_word(grid[r]);  // 격자의 벽과 통로 읽기
    if (grid[0][0] == '#' || grid[rows - 1][cols - 1] == '#') { write_text("-1\n"); return 0; }  // 막힌 끝점은 즉시 제외
    int vertices = rows * cols, answer = -1;  // 상태 수와 아직 없는 도착 답
    const int inf = 1000000;  // 가능한 격자 경로보다 큰 미도달 값
    int dr[4] = {-1, 0, 1, 0}, dc[4] = {0, 1, 0, -1};  // 상·우·하·좌 이동
    for (int v = 0; v < vertices; ++v) distance[v] = inf;  // 모든 칸의 g 초기화
    distance[0] = 0;  // 출발점의 실제 비용
    for (int step = 0; step < vertices; ++step) {  // 각 칸은 최대 한 번 확장
        int u = -1, best = inf;  // 다음 최소 f 후보
        for (int v = 0; v < vertices; ++v) {  // 열린 후보의 f를 직접 비교
            if (closed[v] || distance[v] == inf) continue;  // 닫혔거나 아직 미발견인 칸 제외
            int h = rows - 1 - v / cols + cols - 1 - v % cols;  // 목표까지의 Manhattan 하한
            int score = distance[v] + h;  // A* 우선순위 g+h
            if (score < best) { best = score; u = v; }  // 동률은 작은 칸 번호 유지
        }  // 최소 f 선택 끝
        if (u == -1) break;  // 더 갈 열린 상태가 없음
        if (u == vertices - 1) { answer = distance[u]; break; }  // 목표를 최소 f로 꺼냈을 때만 종료
        closed[u] = 1;  // 일관성으로 현재 g 확정
        int row = u / cols, col = u % cols;  // 번호를 행·열로 복원
        for (int direction = 0; direction < 4; ++direction) {  // 네 방향 전이
            int nr = row + dr[direction], nc = col + dc[direction];  // 이웃 좌표
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == '#') continue;  // 경계와 벽 확인
            int v = nr * cols + nc;  // 이웃의 상태 번호
            if (!closed[v] && distance[u] + 1 < distance[v]) distance[v] = distance[u] + 1;  // 더 좋은 열린 상태의 g 갱신
        }  // 이웃 완화 끝
    }  // 목표 확정 또는 탐색 실패
    write_number(answer); write_text("\n"); return 0;  // 최소 이동 또는 -1 출력
}  // A* 예제 끝
