#include <stdlib.h>

static int compare_int(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    // 음수: x가 앞, 0: 같음, 양수: y가 앞.
    return (x > y) - (x < y);
}

/* Local C function interface. */
int solution(int people[], size_t people_len, int limit) {
    // 원본 배열을 오름차순으로 정렬한다.
    qsort(people, people_len, sizeof(people[0]), compare_int);

    int left = 0;
    int right = (int)people_len - 1;
    int boats = 0;

    while (left <= right) {
        if (left == right) {
            boats++;
            break;
        }

        if (people[left] + people[right] <= limit) {
            // 함께 탈 수 있으면 가장 가벼운 사람도 같이 보낸다.
            left++;
        }
        // 가장 가벼운 사람과도 못 타면 누구와도 함께 탈 수 없다.
        // 가장 무거운 사람은 함께 타든 혼자 타든 이번에 보낸다.
        right--;
        boats++;
    }
    return boats;
}
