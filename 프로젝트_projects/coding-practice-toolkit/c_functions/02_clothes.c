#include <stddef.h>
#include <string.h>

/* Local C function interface. */
int solution(char ***clothes, size_t clothes_rows, size_t clothes_cols) {
    (void)clothes_cols;
    // 원문 제한: 옷 최대 30개, 종류 문자열 최대 20글자 + 종료 문자.
    char categories[30][21];
    int counts[30] = {0};
    int category_count = 0;

    for (size_t i = 0; i < clothes_rows; i++) {
        const char *category = clothes[i][1];
        int index = -1;

        for (int j = 0; j < category_count; j++) {
            // C 문자열은 ==가 아니라 strcmp로 내용을 비교한다.
            if (strcmp(categories[j], category) == 0) {
                index = j;
                break;
            }
        }

        if (index == -1) {
            index = category_count++;
            strcpy(categories[index], category);
        }
        counts[index]++;
    }

    int answer = 1;
    for (int i = 0; i < category_count; i++) {
        // 이 종류의 옷 하나 선택 또는 이 종류는 입지 않는 선택.
        answer *= counts[i] + 1;
    }
    // 전부 입지 않는 조합 하나는 허용되지 않는다.
    return answer - 1;
}
