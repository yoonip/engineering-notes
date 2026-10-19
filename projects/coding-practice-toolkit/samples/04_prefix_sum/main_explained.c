// 자체 창작 연습 04 · 구간 기록 조회 
// 핵심 상태: prefix[i]는 첫 원소부터 i번째 원소까지의 합. 질문 L,R은 1 기반 위치다.
// C11: main이 실행 시작점이다. stdio.h의 scanf/printf로 표준입출력을 사용한다.
// scanf의 %d는 int, %lld는 long long이다. 정수 변수 앞 &는 저장할 주소를 전달한다.
// 문자열 배열 이름은 첫 원소의 주소로 전달된다. 문자열에는 끝의 널 문자 공간이 필요하다.

#include <stdio.h>
// 질문의 위치가 1부터이므로 prefix[0]은 아무 값도 더하지 않은 합 0으로 둔다.
// 최대 N=200000에 0번 칸까지 필요하므로 200001칸을 잡는다.
// 전역 배열의 자동 0 초기화로 prefix[0]=0이다. 큰 구간합은 long long에 담는다.
long long prefix[200001];
int main(void) {
    int n, q, l, r;
    long long x;
    scanf("%d %d", &n, &q);
    // prefix[i-1]에 이번 입력값 x를 더해 prefix[i]를 만든다.
    // 예제 누적합은 0,2,1,5,8,13이다. 음수가 있어도 이 정의는 변하지 않는다.
    // 원본을 다시 다 더하지 않고 처음 한 번의 전처리로 질문을 빨리 처리한다.
    for (int i = 1; i <= n; ++i) {
        scanf("%lld", &x);
        prefix[i] = prefix[i - 1] + x;  // 첫 i개 값의 합.
    }
    // scanf로 L,R을 읽고 prefix[R]-prefix[L-1]을 계산한다.
    // L~R을 포함한 합에서 L 앞까지의 합을 빼는 것이므로 L이 아니라 L-1을 뺀다.
    // L=R인 한 칸 질문과 L=1인 첫 원소부터의 질문도 같은 공식으로 처리된다.
    for (int i = 0; i < q; ++i) {
        scanf("%d %d", &l, &r);
        printf("%lld\n", prefix[r] - prefix[l - 1]);
    }
    return 0;
}

// 복잡도: 시간 O(N+Q), 누적합 공간 O(N). Python은 입력·출력 목록까지 포함해 O(N+Q).
// 마지막 경계 확인:
// - prefix[R]-prefix[L]이 아니라 prefix[R]-prefix[L-1].
// - prefix 배열은 N+1칸이 필요하다.
// - 음수가 있어도 누적합 방식은 정확하다.
