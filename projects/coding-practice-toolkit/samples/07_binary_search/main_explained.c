// 자체 창작 연습 07 · 기준 이상 첫 위치 
// 핵심 상태: 아직 분류하지 않은 원소 구간은 [lo,hi).
// lo 왼쪽은 X보다 작고 hi부터는 X 이상이다.
// lower_bound의 경계 위치 후보에는 hi도 포함된다.
// C11: main이 실행 시작점이다. stdio.h의 scanf/printf로 표준입출력을 사용한다.
// scanf의 %d는 int, %lld는 long long이다. 정수 변수 앞 &는 저장할 주소를 전달한다.
// 문자열 배열 이름은 첫 원소의 주소로 전달된다. 문자열에는 끝의 널 문자 공간이 필요하다.

#include <stdio.h>
int a[200000];
int main(void) {
    int n, q, x;
    scanf("%d %d", &n, &q);
    for (int i = 0; i < n; ++i) scanf("%d", &a[i]);
    while (q--) {
        scanf("%d", &x);
        // lo는 왼쪽 경계, hi는 포함하지 않는 오른쪽 경계다.
        // 처음에는 전체 배열 [0,n)을 검사한다. hi=n은 마지막 원소 다음 위치다.
        // 답이 없으면 n을 출력할 수 있지만 a[n]을 읽어서는 안 된다.
        int lo = 0, hi = n;
        // mid는 남은 구간의 가운데 위치다. lo+(hi-lo)/2 형태로 계산한다.
        // a[mid]>=x면 mid도 후보이므로 hi=mid로 줄인다.
        // a[mid]<x면 mid까지는 답이 아니므로 lo=mid+1로 옮긴다.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] >= x) hi = mid;  // mid도 답 후보이므로 버리지 않는다.
            else lo = mid + 1;
        }
        // lo==hi가 되면 첫 X 이상인 위치를 찾았거나 n까지 도달한 상태다.
        // 이미 정렬되어 있다는 문제 조건이 이분탐색을 가능하게 한다.
        // 중복 X에서 즉시 반환하지 않고 왼쪽 경계를 좁혀 첫 위치를 찾는다.
        printf("%d\n", lo);
    }
    return 0;
}

// 복잡도: 시간 O(N+Q log N), 배열 공간 O(N). Python 전체 파싱·출력 포함 O(N+Q).
// 마지막 경계 확인:
// - 정렬되지 않은 배열에 바로 적용하지 않는다.
// - 인덱스는 0부터 시작한다.
// - hi=N이므로 a[hi]를 직접 읽지 않는다.
// - 중복값에서 찾자마자 종료하면 첫 위치가 아닐 수 있다.
