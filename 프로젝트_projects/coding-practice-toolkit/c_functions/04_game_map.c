#include <stddef.h>

typedef struct {
    int row;
    int col;
} Position;

/* maps is an array of row pointers; dimensions must be 1..100. */
/* Local C function interface. */
int solution(int **maps, size_t maps_rows, size_t maps_cols) {
    int rows = (int)maps_rows;
    int cols = (int)maps_cols;
    int distance[100][100] = {0};

    // 원문 제한은 최대 100 x 100칸. 각 칸은 최대 한 번 들어간다.
    Position queue[10000];
    int head = 0;
    int tail = 0;
    int dr[4] = {-1, 1, 0, 0};
    int dc[4] = {0, 0, -1, 1};

    if (maps[0][0] == 0 || maps[rows - 1][cols - 1] == 0) return -1;

    distance[0][0] = 1; // 시작 칸도 지나온 칸 수에 포함한다.
    queue[tail++] = (Position){0, 0};

    while (head < tail) {
        // 먼저 넣은 칸부터 꺼내므로 가까운 칸부터 탐색한다.
        Position current = queue[head++];
        int row = current.row;
        int col = current.col;

        if (row == rows - 1 && col == cols - 1) return distance[row][col];

        for (int direction = 0; direction < 4; direction++) {
            int nr = row + dr[direction];
            int nc = col + dc[direction];
            // 범위를 확인한 뒤에 배열을 접근해야 한다.
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            if (maps[nr][nc] == 0 || distance[nr][nc] != 0) continue;

            // 큐에 넣을 때 방문 표시해 중복 삽입을 막는다.
            distance[nr][nc] = distance[row][col] + 1;
            queue[tail++] = (Position){nr, nc};
        }
    }
    return -1; // 모든 접근 가능한 칸을 탐색해도 도착하지 못했다.
}
