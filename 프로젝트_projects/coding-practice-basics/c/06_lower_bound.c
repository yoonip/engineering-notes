#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2 || n <= 0 || q <= 0) return 0;

    long long *values = malloc((size_t)n * sizeof(*values));
    if (values == NULL) return 1;
    for (int i = 0; i < n; ++i) scanf("%lld", &values[i]);

    for (int query = 0; query < q; ++query) {
        long long target;
        scanf("%lld", &target);

        int low = 0, high = n; /* 탐색 구간은 [low, high) */
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (values[mid] < target) low = mid + 1;
            else high = mid;
        }

        int answer = (low < n && values[low] == target) ? low : -1;
        printf("%d\n", answer);
    }

    free(values);
    return 0;
}
