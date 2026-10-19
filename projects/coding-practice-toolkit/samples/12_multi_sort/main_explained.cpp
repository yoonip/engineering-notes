// 점수 내림차순, 점수 동점일 때 이름 오름차순으로 기록을 정렬한다.
// 중복 기록도 입력된 개수만큼 남겨야 하므로 집합으로 중복을 지우지 않는다.
// 이름은 영문 소문자만 허용하여 세 언어에서 같은 사전순으로 비교된다.
// 입력 제한과 실행 비용: 이름 최대 길이 L≤20. C++/Python O(N log N·L), 공간 O(NL). C qsort는 C 표준에 시간복잡도 보장이 없고 일반 구현은 O(N log N) 정렬이 흔하다. 이름 비교 자체는 O(L)이다.

// Record 또는 튜플 한 개가 점수와 이름을 함께 보관한다.
// C의 name[21]은 최대 20글자와 끝의 널 문자를 위한 공간이다.
// 점수는 음수도 가능하다. Python의 -score는 높은 점수가 작은 키로 먼저 오게 만든다.

// vector는 실행 중 정해진 크기의 배열, queue는 먼저 넣은 원소를 먼저 꺼내는 큐다.
// 사용한 컨테이너와 헤더는 이 원문 그대로 따른다. 빠른 cin 설정 뒤에는 scanf와 섞지 않는다.

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
struct Record { int score; string name; };
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; cin >> n;
    vector<Record> a(n);
    // 점수와 이름을 같은 기록에 묶어 저장한다.
    // C %20s는 이름 버퍼 크기를 지키고, Python은 읽은 바이트를 문자열로 바꿔 저장한다.
    for (auto &x:a) cin >> x.score >> x.name;
    // 첫 기준 점수를 먼저 비교하고 동점에서만 이름을 비교한다.
    // C qsort의 비교함수는 음수/0/양수, C++ sort 비교함수는 앞에 와야 하는지의 참/거짓을 반환한다.
    // C++은 완전히 같은 기록끼리 false여야 하고 Python은 (-점수,이름)을 오름차순 정렬한다.
    sort(a.begin(), a.end(), [](const Record &x, const Record &y) {
        // 다른 점수에서는 높은 점수가 먼저 온다.
        // C에서 점수를 단순히 뺄셈해 비교 부호를 만들면 자료형 범위에 따라 넘칠 수 있어 대소를 직접 비교한다.
        if (x.score != y.score) return x.score > y.score;
        // 점수가 같을 때 이름을 오름차순으로 비교한다.
        // 점수와 이름이 모두 같으면 같은 출력 기록이므로 내부 순서가 달라도 결과는 같다.
        return x.name < y.name;
    });
    // 정렬 결과를 기록 단위로 출력한다.
    // 전체 키에 reverse를 적용하면 이름까지 뒤집히므로 Python은 점수 부호만 바꾼다.
    for (const auto &x:a)
        cout << x.score << ' ' << x.name << '\n';
}

// 손으로 확인: 95점 기록: bob,amy,amy → amy,amy,bob
// 손으로 확인: 80점 기록: zoe,ann → ann,zoe
// 손으로 확인: 95점 그룹이 80점 그룹보다 앞
// 완성 후 확인: C 비교함수는 점수의 단순 뺄셈보다 대소 비교로 부호를 반환한다.
// 완성 후 확인: C++ 비교함수에서 같은 기록끼리는 false를 반환해야 한다.
// 완성 후 확인: 이름 오름차순 조건을 빠뜨리지 않는다.
// 완성 후 확인: 이 문제의 이름은 영문 소문자로 제한해 세 언어의 비교 규칙을 일치시켰다.
