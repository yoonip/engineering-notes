// 자체 창작 연습 04 · 구간 기록 조회 
// 핵심 상태: prefix[i]는 첫 원소부터 i번째 원소까지의 합. 질문 L,R은 1 기반 위치다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, l, r;
    cin >> n >> q;
    // n+1칸을 만들고 모든 원소를 0으로 초기화한다.
    // 0번 칸은 기준점이고 1~n번 칸이 실제 앞부분 합을 저장한다.
    // vector<long long>으로 큰 합을 담는다. 질문의 인덱스는 int여도 충분하다.
    vector<long long> prefix(n + 1, 0);
    long long x;
    // prefix[i]에 첫 i개 값의 합을 저장한다.
    // 앞에 이미 계산한 합 prefix[i-1]을 재사용한다.
    // 데이터가 변경되지 않는 문제이므로 이후 모든 질문에 같은 누적합을 쓸 수 있다.
    for (int i = 1; i <= n; ++i) {
        cin >> x;
        prefix[i] = prefix[i - 1] + x;
    }
    // q--는 기존 q 값을 조건으로 검사한 뒤 q를 1 줄인다. 초기 q가 양수라 정확히 q회 실행된다.
    // 매 질문은 L,R 두 정수를 입력받아 양 끝 포함 구간합을 출력한다.
    // prefix[R]-prefix[L-1] 한 번이면 질문 하나가 O(1)이다.
    while (q--) {
        cin >> l >> r;
        cout << prefix[r] - prefix[l - 1] << '\n';  // L~R 양 끝 포함.
    }
}

// 복잡도: 시간 O(N+Q), 누적합 공간 O(N). Python은 입력·출력 목록까지 포함해 O(N+Q).
// 마지막 경계 확인:
// - prefix[R]-prefix[L]이 아니라 prefix[R]-prefix[L-1].
// - prefix 배열은 N+1칸이 필요하다.
// - 음수가 있어도 누적합 방식은 정확하다.
