#include <stdlib.h>

/* Local C function interface. */
int *solution(int progresses[], size_t progresses_len,
              int speeds[], size_t speeds_len, size_t *answer_len) {
    (void)speeds_len;
    *answer_len = 0;
    if (progresses_len == 0) return NULL;

    // 결과 배열은 함수가 끝난 뒤에도 살아 있어야 하므로 malloc을 사용한다.
    int *answer = malloc(progresses_len * sizeof(*answer));
    if (answer == NULL) return NULL;

    int release_day = 0;
    int count = 0;

    for (size_t i = 0; i < progresses_len; i++) {
        // 양의 정수 나눗셈의 올림: 남은 작업 70, 속도 30이면 3일.
        int remaining = 100 - progresses[i];
        int day = (remaining + speeds[i] - 1) / speeds[i];

        if (count == 0) {
            release_day = day;
            count = 1;
        } else if (day <= release_day) {
            // 먼저 끝난 뒤 작업도 앞 작업의 배포일에 함께 배포한다.
            count++;
        } else {
            answer[(*answer_len)++] = count;
            release_day = day;
            count = 1;
        }
    }

    answer[(*answer_len)++] = count;
    // 호출한 쪽에서 사용 후 free(answer)한다. 여기서 해제하면 안 된다.
    return answer;
}
