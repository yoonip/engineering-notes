// 자체 창작 연습 07 · 기준 이상 첫 위치 
// 핵심 상태: 아직 분류하지 않은 원소 구간은 [lo,hi).
// lo 왼쪽은 X보다 작고 hi부터는 X 이상이다.
// lower_bound의 경계 위치 후보에는 hi도 포함된다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, q, x;
    cin >> n >> q;
    // 정렬된 정수 n개를 vector에 저장한다. 입력 순서를 그대로 보관한다.
    // 이 문제의 인덱스는 0 기반이며 X는 값이지 위치가 아니다.
    // 다른 문제에서 정렬되지 않았다면 먼저 정렬해야 같은 이분탐색 논리를 쓸 수 있다.
    vector<int> a(n);
    for (int &v : a) cin >> v;
    while (q--) {
        cin >> x;
        // [lo,hi)는 lo를 포함하고 hi는 포함하지 않는 구간이다.
        // a[mid]>=x면 hi=mid, 아니면 lo=mid+1로 답 후보를 줄인다.
        // lo==hi까지 좁히면 동일한 값이 반복되어도 첫 위치를 얻는다.
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid] >= x) hi = mid;
            else lo = mid + 1;  // mid까지는 X보다 작아 후보에서 제외한다.
        }
        // 각 질문의 결과를 한 줄에 하나씩 출력한다.
        // lo가 n이면 X 이상인 원소가 없다는 뜻이다. 출력 전에 a[lo]를 읽지 않는다.
        // 표준 lower_bound도 같은 의미지만 여기서는 갱신 규칙을 익히기 위해 직접 구현했다.
        cout << lo << '\n';
    }
}

// 복잡도: 시간 O(N+Q log N), 배열 공간 O(N). Python 전체 파싱·출력 포함 O(N+Q).
// 마지막 경계 확인:
// - 정렬되지 않은 배열에 바로 적용하지 않는다.
// - 인덱스는 0부터 시작한다.
// - hi=N이므로 a[hi]를 직접 읽지 않는다.
// - 중복값에서 찾자마자 종료하면 첫 위치가 아닐 수 있다.
