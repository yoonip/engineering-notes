// 자체 창작 연습 08 · 목표 합의 연속 구간 
// 핵심 상태: [left,right]가 현재 연속 구간, window가 그 합, answer가 찾은 구간 개수다.
// C11: main이 실행 시작점이다. stdio.h의 scanf/printf로 표준입출력을 사용한다.
// scanf의 %d는 int, %lld는 long long이다. 정수 변수 앞 &는 저장할 주소를 전달한다.
// 문자열 배열 이름은 첫 원소의 주소로 전달된다. 문자열에는 끝의 널 문자 공간이 필요하다.

#include <stdio.h>
long long a[200000];
int main(void) {
    int n, left = 0;
    // 목표 k와 구간합 window는 최대 2×10^14까지 가므로 long long으로 둔다.
    // left는 현재 구간의 첫 위치이고 right는 반복마다 새로 포함할 마지막 위치다.
    // 처음에는 아무 값도 포함하지 않아 window=0이고 발견한 구간 수도 0이다.
    long long k, window = 0, answer = 0;
    scanf("%d %lld", &n, &k);
    for (int i = 0; i < n; ++i) scanf("%lld", &a[i]);
    // 오른쪽 끝을 앞으로 한 칸씩 늘리며 이번 원소를 window에 더한다.
    // 합이 목표보다 크면 왼쪽 원소를 빼며 left를 앞으로 옮긴다.
    // 원소가 모두 양수이므로 오른쪽 확대는 합 증가, 왼쪽 축소는 합 감소다. 이 조건이 핵심이다.
    for (int right = 0; right < n; ++right) {
        window += a[right];
        // 합이 너무 크면 한 번만이 아니라 충분히 작아질 때까지 반복해서 뺀다.
        // a[left]를 뺀 후 left++로 다음 위치를 왼쪽 끝으로 만든다.
        // 합이 k가 되면 같은 right에서 가능한 구간을 하나 센다. 양수 조건으로 왼쪽 끝은 유일하다.
        while (left <= right && window > k)
            window -= a[left++];  // 현재 왼쪽 값을 뺀 뒤 left를 증가시킨다.
        if (window == k) ++answer;
    }
    printf("%lld\n", answer);
    return 0;
}

// 복잡도: 시간 O(N), 저장 배열 공간 O(N). 이중 반복문이 있어도 각 원소를 한 번 넣고 한 번 뺀다.
// 마지막 경계 확인:
// - 양수 조건을 확인한다.
// - K와 window는 C/C++ long long.
// - window>K일 때 한 번만 빼지 말고 while로 충분히 줄인다.
// - 부분배열은 연속이고, 부분집합과 다르다.
