// 자체 창작 연습 01 · 숫자 기록의 합 
// 핵심 상태: total은 지금까지 읽은 숫자의 합, x는 이번에 읽은 숫자, n은 숫자 개수다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    // 입력값과 누적합은 long long에 저장해 큰 합을 안전하게 담는다.
    // total=0은 아무 숫자도 처리하지 않은 상태의 합이다.
    // x는 반복마다 새 입력값으로 바뀌고 total은 지금까지의 합을 유지한다.
    long long x, total = 0;
    // cin >> n은 입력에서 정수 하나를 읽어 n에 저장한다.
    // C scanf와 달리 이 형태는 &n이나 %d를 적지 않는다.
    // n은 개수이므로 뒤의 n개 숫자만 실제 합산 대상으로 삼는다.
    cin >> n;
    // 반복의 각 단계는 숫자 하나 읽기와 합에 더하기다.
    // 예제에서 3을 읽으면 total=3, -2를 읽으면 total=1이 된다.
    // n개를 모두 처리한 뒤 한 번만 출력하므로 중간 합은 출력하지 않는다.
    for (int i = 0; i < n; ++i) {
        cin >> x;
        total += x;  // total = total + x와 같은 뜻이다.
    }
    cout << total << '\n';
}

// 복잡도: 시간 O(N). C/C++는 입력을 즉시 더해 추가 공간 O(1); Python 예제는 전체 입력 파싱으로 O(N).
// 마지막 경계 확인:
// - C에서 long long 입력은 %lld, 출력도 %lld.
// - 입력 N을 합에 포함하지 않는다.
// - 출력에 설명 문장을 붙이지 않는다.
