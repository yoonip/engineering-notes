#include <stdio.h>

int main(void) {
    static char digits[200001];
    int frequency[10] = {0};

    if (scanf("%200000s", digits) != 1) return 0;

    for (int i = 0; digits[i] != '\0'; ++i) {
        if (digits[i] >= '0' && digits[i] <= '9') {
            ++frequency[digits[i] - '0'];
        }
    }

    for (int digit = 0; digit < 10; ++digit) {
        if (digit > 0) putchar(' ');
        printf("%d", frequency[digit]);
    }
    putchar('\n');
    return 0;
}
