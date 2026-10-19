// 길이 W인 연속 구간의 최대 합과 가장 앞 시작 위치를 찾는다.
// 창을 한 칸 옮길 때 빠진 값을 빼고 들어온 값을 더하므로 매번 W개를 다시 더하지 않는다.
// 음수만 있어도 실제 구간 하나를 골라야 하며, 동점에서는 앞 구간을 유지한다.
// 입력 제한과 실행 비용: 시간 O(N), 공간 O(N).

// window는 현재 정확히 W개 원소의 합, best는 지금까지의 최대 구간합이다.
// start는 출력할 1 기반 시작 위치다. 첫 구간의 시작은 1이다.
// 합의 절댓값은 최대 200,000×1,000,000,000이다. C/C++은 long long이 필요하다.

// vector는 실행 중 정해진 크기의 배열, queue는 먼저 넣은 원소를 먼저 꺼내는 큐다.
// 사용한 컨테이너와 헤더는 이 원문 그대로 따른다. 빠른 cin 설정 뒤에는 scanf와 섞지 않는다.

#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,w,start=1; cin >> n >> w;
    vector<long long> a(n);
    for (auto &x:a) cin >> x;
    long long window=0;
    // 먼저 첫 W개의 합으로 실제 첫 구간을 만든다.
    // best를 0으로 두면 모든 합이 음수일 때 존재하지 않는 답 0을 고르게 된다.
    for (int i=0; i<w; ++i) window+=a[i];
    long long best=window; // 실제 첫 구간합으로 초기화하므로 음수에서도 올바르다.
    // i는 새로 들어오는 원소의 0 기반 위치다.
    // 이전 창에서 a[i-w]가 빠지고 a[i]가 들어오므로 창 길이는 W로 유지된다.
    // 새 창의 0 기반 시작 i-w+1을 출력용 1 기반으로 바꾸면 i-w+2다.
    for (int i=w; i<n; ++i) {
        window+=a[i]-a[i-w]; // 새 원소 더하기 - 빠진 원소 빼기로 O(1)에 다음 합을 만든다.
        // 엄격히 더 큰 합일 때만 답을 갱신한다.
        // 같은 합에는 갱신하지 않아 먼저 찾은, 가장 앞쪽 구간이 남는다.
        if (window>best) { best=window; start=i-w+2; }
    }
    cout << best << ' ' << start << '\n';
}

// 손으로 확인: W=3의 구간합: 5,0,6,3
// 손으로 확인: 세 번째 구간 4,-3,5의 합6
// 손으로 확인: 출력 6 3
// 완성 후 확인: 첫 구간합으로 best를 초기화한다.
// 완성 후 확인: 출력 인덱스는 1 기반.
// 완성 후 확인: 창 크기는 반드시 W로 유지된다.
