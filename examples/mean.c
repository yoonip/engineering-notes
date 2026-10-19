#include <stddef.h>
#include <stdio.h>

double mean(const double *values, size_t count) {
    double sum = 0.0;
    for (size_t i = 0; i < count; ++i) {
        sum += values[i];
    }
    return sum / (double)count;
}

int main(void) {
    const double voltage[] = {3.1, 3.2, 3.3};
    const size_t count = sizeof voltage / sizeof voltage[0];
    printf("%.3f V\n", mean(voltage, count));
    return 0;
}
