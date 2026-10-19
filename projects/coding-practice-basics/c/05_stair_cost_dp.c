#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;

    long long *cost = malloc((size_t)n * sizeof(*cost));
    long long *best = malloc((size_t)n * sizeof(*best));
    if (cost == NULL || best == NULL) {
        free(cost); free(best);
        return 1;
    }

    for (int i = 0; i < n; ++i) scanf("%lld", &cost[i]);

    best[0] = cost[0];
    if (n >= 2) best[1] = cost[0] + cost[1];
    for (int i = 2; i < n; ++i) {
        long long previous = best[i - 1] < best[i - 2] ? best[i - 1] : best[i - 2];
        best[i] = previous + cost[i];
    }

    printf("%lld\n", best[n - 1]);
    free(cost); free(best);
    return 0;
}
