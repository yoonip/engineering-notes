// 자체 창작 연습 05 · 괄호 짝 검사 
// 핵심 상태: stack/st에는 아직 닫히지 않은 여는 괄호를 저장한다. top 또는 길이가 스택 크기다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <string>
#include <vector>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    // vector를 여기서는 끝에만 넣고 빼는 스택으로 사용한다.
    // push_back은 여는 괄호를 쌓고 pop_back은 가장 최근 괄호를 제거한다.
    // string은 문자열 길이를 관리해 C의 널 문자 반복을 직접 쓸 필요가 없다.
    vector<char> stack;
    bool ok = true;
    cin >> s;
    // 문자열의 각 문자 ch를 한 번씩 읽는다.
    // 여는 괄호는 넣고, 닫는 괄호는 stack.empty()를 먼저 검사해 짝이 존재하는지 확인한다.
    // empty인 vector에 pop_back을 하면 유효한 연산이 아니므로 반드시 순서를 지킨다.
    for (char ch : s) {
        if (ch == '(') stack.push_back(ch);
        else if (stack.empty()) { ok = false; break; }
        else stack.pop_back();  // 가장 최근 여는 괄호 하나를 짝지어 제거한다.
    }
    // 문자열이 끝난 뒤 아직 남은 여는 괄호가 있는지도 확인한다.
    // !는 논리 부정이므로 !stack.empty()는 스택이 비어 있지 않다는 뜻이다.
    // cout은 조건에 따라 YES 또는 NO만 출력한다.
    if (!stack.empty()) ok = false;
    cout << (ok ? "YES" : "NO") << '\n';
}

// 복잡도: 시간 O(S), 공간 O(S). S는 문자열 길이.
// 마지막 경계 확인:
// - 끝에 남은 여는 괄호도 검사한다.
// - 스택이 빈 상태에서 pop하지 않는다.
// - 여는 괄호 수와 닫는 괄호 수만 같다고 올바른 것은 아니다: )(는 NO.
