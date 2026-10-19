#include <stdio.h>
#include <stdlib.h>

static int compare_long_long(const void *left, const void *right) {
    long long a = *(const long long *)left;
    long long b = *(const long long *)right;
    return (a > b) - (a < b);
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;

    long long *values = malloc((size_t)n * sizeof(*values));
    if (values == NULL) return 1;

    for (int i = 0; i < n; ++i) scanf("%lld", &values[i]);
    qsort(values, (size_t)n, sizeof(*values), compare_long_long);

    for (int i = 0; i < n; ++i) {
        if (i > 0) putchar(' ');
        printf("%lld", values[i]);
    }
    putchar('\n');

    free(values);
    return 0;
}
