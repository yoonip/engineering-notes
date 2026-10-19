// 자체 창작 연습 08 · 목표 합의 연속 구간 
// 핵심 상태: [left,right]가 현재 연속 구간, window가 그 합, answer가 찾은 구간 개수다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, left = 0;
    long long k, window = 0, answer = 0;
    cin >> n >> k;
    // 두 포인터가 이전 값을 다시 빼야 하므로 입력 전체를 배열에 보관한다.
    // 입력과 구간합은 long long으로 두어 큰 목표를 처리한다.
    // for(auto &x:a)의 참조 &는 vector의 원소에 직접 입력을 저장하기 위해 필요하다.
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    // right를 한 칸 앞으로 옮기며 새 값을 합에 더한다.
    // 목표를 넘으면 left를 옮겨 합을 줄인다. 두 끝점 모두 뒤로 돌아가지 않는다.
    // 이중 반복처럼 보여도 각 원소를 한 번 넣고 한 번 빼서 총 O(N)이다.
    for (int right = 0; right < n; ++right) {
        window += a[right];  // 오른쪽 새 원소를 현재 구간에 포함한다.
        while (left <= right && window > k)
            window -= a[left++];
        // window가 k면 [left,right]라는 위치 구간 하나를 발견했다.
        // 같은 값들이 있어도 위치가 다르면 서로 다른 구간으로 센다.
        // 음수나 0이 허용되는 문제에는 이 개수 세기 코드를 그대로 적용하지 않는다.
        if (window == k) ++answer;
    }
    cout << answer << '\n';
}

// 복잡도: 시간 O(N), 저장 배열 공간 O(N). 이중 반복문이 있어도 각 원소를 한 번 넣고 한 번 뺀다.
// 마지막 경계 확인:
// - 양수 조건을 확인한다.
// - K와 window는 C/C++ long long.
// - window>K일 때 한 번만 빼지 말고 while로 충분히 줄인다.
// - 부분배열은 연속이고, 부분집합과 다르다.
