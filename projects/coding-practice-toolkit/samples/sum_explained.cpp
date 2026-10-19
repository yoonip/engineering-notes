// 시작 예제: 첫 수 N과 뒤의 N개 값을 읽어 합을 출력합니다.
// iostream은 cin(입력), cout(출력)을 제공합니다. using은 std:: 접두어를 생략하게 합니다.
#include <iostream>
using namespace std;

int main() {
    // C 입출력과의 동기화를 끄고 cin과 cout의 자동 flush 연결을 풉니다.
    // 입력이 많은 코딩테스트의 속도 설정입니다. 여기서는 scanf/printf와 섞지 않습니다.
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;  // 입력 실패라면 n을 사용하지 않고 끝냅니다.
    long long sum = 0, value;  // N은 개수, sum은 지금까지 읽은 값의 합입니다.
    for (int i = 0; i < n; ++i) {
        if (!(cin >> value)) return 1;
        sum += value;  // 예: 1,2,3을 읽었을 때 합은 1→3→6입니다.
    }
    cout << sum << '\n';  // 답 하나만 출력합니다. 설명 문구를 출력하면 온라인 채점에서 틀릴 수 있습니다.
    return 0;
}
// cin은 필요한 N개 값을 읽으면 계산을 마칩니다. Python read()처럼 반드시 EOF를 기다리는 구조가 아닙니다.
// F5/ Ctrl+F5에서는 이 폴더 input.txt를 자동으로 사용합니다. 시간 O(N), 추가 메모리 O(1).
