// 자체 창작 연습 09 · 최소 동전 개수 
// 핵심 상태: dp[x]는 금액 x를 만드는 최소 동전 개수. inf는 만들 수 없음, dp[0]=0이다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, k, inf = 10001;
    cin >> n >> k;
    // coin은 n개 금액, dp는 0~k까지 k+1개 상태다.
    // dp를 모두 inf로 시작한 뒤 dp[0]만 0으로 바꿔 출발 상태를 만든다.
    // 0원은 동전을 쓰지 않는 것이 최솟값 0이며 k=0도 같은 초기값으로 해결된다.
    vector<int> coin(n), dp(k + 1, inf);
    for (int &c : coin) cin >> c;
    dp[0] = 0;  // 아무 동전도 쓰지 않고 0원을 만든다.
    // 금액을 작은 순서대로 만들며 각 동전 c를 마지막으로 써 보는 후보를 비교한다.
    // dp[x-c]는 더 작은 금액이어서 이미 계산되어 있다.
    // 같은 종류를 무제한 쓸 수 있다. 한 번씩만 사용 가능한 문제와 상태 갱신이 다르다.
    for (int x = 1; x <= k; ++x)
        for (int c : coin)
            if (c <= x && dp[x-c] + 1 < dp[x])
                dp[x] = dp[x-c] + 1;
    // ?:는 조건이 참일 때 앞 값, 거짓일 때 뒤 값을 고르는 조건 연산자다.
    // 끝까지 inf인 목표는 만들 수 없으므로 -1로 출력한다.
    // 큰 동전부터 고르는 그리디는 1,3,4로 6을 만들 때 최적 답 3+3을 놓친다.
    cout << (dp[k] == inf ? -1 : dp[k]) << '\n';
}

// 복잡도: 시간 O(NK), 공간 O(N+K).
// 마지막 경계 확인:
// - 동전은 무제한 사용 가능하다. 한 번씩만 쓰는 문제와 다르다.
// - dp를 0으로 채우면 불가능한 금액도 가능하다고 처리된다.
// - x-c가 음수인 후보는 건너뛴다.
// - INF=K+1도 가능하지만 여기서는 제한에 맞춰 10001을 쓴다.
