// 자체 창작 연습 03 · 작업 완료시간 합 최소화 
// 핵심 상태: elapsed는 현재 작업까지의 완료시각, answer는 모든 완료시각의 누적합이다.
// C11: main이 실행 시작점이다. stdio.h의 scanf/printf로 표준입출력을 사용한다.
// scanf의 %d는 int, %lld는 long long이다. 정수 변수 앞 &는 저장할 주소를 전달한다.
// 문자열 배열 이름은 첫 원소의 주소로 전달된다. 문자열에는 끝의 널 문자 공간이 필요하다.

#include <stdio.h>
#include <stdlib.h>
int a[200000];
// qsort는 원소의 타입을 모르므로 비교할 두 원소의 주소를 void 포인터로 받는다.
// const int *로 해석한 뒤 *로 해당 주소의 실제 정수 값을 읽는다.
// 음수/0/양수 반환은 앞 원소가 작음/같음/큼을 뜻한다. 큰 값의 단순 뺄셈을 피한다.
int cmp(const void *p, const void *q) {
    int x = *(const int *)p, y = *(const int *)q;
    return (x > y) - (x < y);
}
int main(void) {
    int n;
    long long elapsed = 0, answer = 0;
    scanf("%d", &n);
    for (int i = 0; i < n; ++i) scanf("%d", &a[i]);
    // a의 첫 주소, 원소 개수 n, 원소 한 개의 바이트 크기, 비교함수를 전달한다.
    // 수행시간을 오름차순으로 정렬해 짧은 작업부터 처리한다.
    // C 표준은 qsort의 시간복잡도를 명시하지 않는다. 구현의 정렬 동작과 알고리즘 근거를 구분한다.
    qsort(a, n, sizeof(a[0]), cmp);
    // 정렬 뒤 수행시간 1,2,3,3,4를 차례대로 더해 완료시각 1,3,6,9,13을 만든다.
    // 각 완료시각을 answer에 더하면 32가 된다. 자기 수행시간도 포함한다.
    // elapsed와 answer는 합이 커질 수 있으므로 long long으로 선언했다.
    for (int i = 0; i < n; ++i) {
        elapsed += a[i];
        answer += elapsed;  // 이번 작업의 완료시각을 전체 합에 포함한다.
    }
    printf("%lld\n", answer);
    return 0;
}

// 복잡도: 일반적인 정렬 구현에서 시간 O(N log N), 공간 O(N). C 표준 qsort는 표준 자체가 최악 시간 복잡도를 보장하지 않는다.
// 마지막 경계 확인:
// - 완료시각과 대기시간을 구분한다. 이 문제는 자기 수행시간을 포함한다.
// - answer와 elapsed는 long long을 사용한다.
// - C qsort 비교함수에서 큰 정수의 단순 뺄셈은 일반적으로 오버플로 위험이 있다. 비교식을 쓴다.
