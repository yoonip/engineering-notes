// 자체 창작 연습 10 · 목표 합의 부분집합 
// 핵심 상태: dfs(i,total,used)는 i번째부터 결정할 차례. total은 선택 합, used는 하나 이상 선택 여부다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
using namespace std;
int n;
long long target, answer = 0;
vector<long long> a;
// i,total,used는 각 호출마다 값으로 전달되는 상태다.
// bool used는 현재 선택에 원소가 하나 이상 있는지를 나타낸다.
// 벡터 a와 target은 모든 호출이 함께 읽고 answer는 전체 개수를 누적한다.
void dfs(int i, long long total, bool used) {
    // i==n이면 더 선택할 원소가 없고 결과를 검사할 때다.
    // used && total==target으로 빈 집합을 제외한다. 특히 target=0에서 중요하다.
    // 끝난 호출은 return하고 이전 호출로 돌아가 다른 가지를 탐색한다.
    if (i == n) {
        if (used && total == target) ++answer;
        return;
    }
    // 선택/미선택 두 호출이 각 원소마다 두 갈래를 만든다.
    // N≤20이라 최대 2^20개 선택을 볼 수 있으며 재귀 깊이는 N이다.
    // 같은 값도 위치가 다르면 다른 원소로 취급한다. 값을 중복 제거해서는 안 된다.
    dfs(i + 1, total + a[i], true);
    dfs(i + 1, total, used);  // 현재 위치를 고르지 않는 가지.
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    cin >> n >> target;
    a.resize(n);
    for (auto &x : a) cin >> x;
    dfs(0, 0, false);
    cout << answer << '\n';
}

// 복잡도: 시간 O(2^N), 재귀 깊이 및 배열 공간 O(N). 재귀 깊이가 20이므로 이 예제는 Python 재귀 한도 변경이 필요 없다.
// 마지막 경계 확인:
// - T=0에서 빈 집합을 세지 않는다.
// - 같은 값을 가진 서로 다른 위치를 임의로 합치지 않는다.
// - 연속 구간 개수와 부분집합 개수를 구분한다.
// - 합은 C/C++ long long으로 받는다.
