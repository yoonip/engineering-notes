#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1 || n <= 0) return 0;

    long long *values = malloc((size_t)n * sizeof(*values));
    if (values == NULL) return 1;

    long long minimum = LLONG_MAX;
    long long maximum = LLONG_MIN;
    long long sum = 0;

    for (int i = 0; i < n; ++i) {
        scanf("%lld", &values[i]);
        if (values[i] < minimum) minimum = values[i];
        if (values[i] > maximum) maximum = values[i];
        sum += values[i];
    }

    printf("%lld %lld %lld\n", minimum, maximum, sum);
    free(values);
    return 0;
}
