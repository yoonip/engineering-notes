#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2 || n <= 0 || m <= 0) return 0;

    int cells = n * m;
    char *grid = malloc((size_t)cells * sizeof(*grid));
    char *row = malloc((size_t)m + 1);
    int *distance = calloc((size_t)cells, sizeof(*distance));
    int *queue = malloc((size_t)cells * sizeof(*queue));
    if (grid == NULL || row == NULL || distance == NULL || queue == NULL) {
        free(grid); free(row); free(distance); free(queue);
        return 1;
    }

    for (int r = 0; r < n; ++r) {
        scanf("%s", row);
        memcpy(grid + r * m, row, (size_t)m);
    }

    int answer = -1;
    if (grid[0] == '1') {
        int head = 0, tail = 0;
        queue[tail++] = 0;
        distance[0] = 1;

        while (head < tail) {
            int here = queue[head++];
            int r = here / m;
            int c = here % m;

            if (here == cells - 1) {
                answer = distance[here];
                break;
            }

            int next[4];
            int count = 0;
            if (r > 0) next[count++] = here - m;
            if (r + 1 < n) next[count++] = here + m;
            if (c > 0) next[count++] = here - 1;
            if (c + 1 < m) next[count++] = here + 1;

            for (int i = 0; i < count; ++i) {
                int there = next[i];
                if (grid[there] == '1' && distance[there] == 0) {
                    distance[there] = distance[here] + 1;
                    queue[tail++] = there;
                }
            }
        }
    }

    printf("%d\n", answer);
    free(grid); free(row); free(distance); free(queue);
    return 0;
}
