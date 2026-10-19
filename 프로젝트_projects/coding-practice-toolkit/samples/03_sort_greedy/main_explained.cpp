// 자체 창작 연습 03 · 작업 완료시간 합 최소화 
// 핵심 상태: elapsed는 현재 작업까지의 완료시각, answer는 모든 완료시각의 누적합이다.
// C++17: main이 실행 시작점이다. cin/cout은 변수 타입에 맞게 입력·출력을 처리한다.
// sync_with_stdio(false), cin.tie(nullptr)는 많은 입출력의 불필요한 동기화·flush를 줄인다.
// 이 설정을 사용한 뒤 scanf와 cin을 섞지 않는 방식으로 연습한다.

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    // vector<int>는 n개 정수를 담는 표준 가변 배열이다.
    // for(int &x:a)의 &x는 각 원소 자체를 가리키는 참조여서 cin으로 원본 배열에 저장된다.
    // 값 복사인 for(int x:a)로 입력하면 x만 바뀌고 배열에는 저장되지 않는다.
    vector<int> a(n);
    for (int &x : a) cin >> x;
    // begin은 첫 위치, end는 마지막 원소 다음 위치다. [begin,end)를 정렬한다.
    // 기본 sort는 작은 수행시간부터 오름차순으로 배치한다.
    // 짧은 작업을 앞에 두면 뒤의 많은 작업이 덜 기다려 완료시각 합이 최소가 된다.
    sort(a.begin(), a.end());
    long long elapsed = 0, answer = 0;
    // 이번 반복은 읽기만 하므로 int x로 원소 값을 복사해도 충분하다.
    // elapsed에 x를 더해 이번 완료시각을 만든 뒤 answer에 그 값을 더한다.
    // 단순 수행시간 합과 모든 완료시각 합은 다르다. 예제 정답은 13이 아니라 32다.
    for (int x : a) {
        elapsed += x;
        answer += elapsed;  // 수행시간 x 자체가 아니라 완료시각을 더한다.
    }
    cout << answer << '\n';
}

// 복잡도: 일반적인 정렬 구현에서 시간 O(N log N), 공간 O(N). C 표준 qsort는 표준 자체가 최악 시간 복잡도를 보장하지 않는다.
// 마지막 경계 확인:
// - 완료시각과 대기시간을 구분한다. 이 문제는 자기 수행시간을 포함한다.
// - answer와 elapsed는 long long을 사용한다.
// - C qsort 비교함수에서 큰 정수의 단순 뺄셈은 일반적으로 오버플로 위험이 있다. 비교식을 쓴다.
