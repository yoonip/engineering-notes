// PDF의 함수 코드를 PC에서 실행할 수 있도록 입력용 main을 추가했습니다.
// 함수가 계산한 값을 return으로 전달하고, main이 cout으로 출력합니다.
// 실제 온라인 함수형 문제는 제공된 함수 이름·인자·반환형을 그대로 맞춥니다.
#include <iostream>
#include <vector>
// const 참조(&)로 받아 전체 vector를 복사하지 않습니다. const이므로 이 함수에서 원소를 바꾸지 않습니다.
long long total(const std::vector<int>& a) {
    long long ans = 0;  // 큰 합을 저장할 누적 값.
    for (int x : a) ans += x;  // 범위 for가 각 원소의 값을 x에 복사해 한 번씩 처리합니다.
    return ans;  // 호출한 식의 값이 ans가 됩니다. print나 cout과 역할이 다릅니다.
}
// 독립 실행용 입력·출력 코드입니다. 온라인 함수형 제출에는 보통 이 부분이 없습니다.
int main() {
    int n;
    if (!(std::cin >> n)) return 0;
    if (n < 0 || n > 100000) return 1;
    std::vector<int> a(n);  // N칸짜리 동적 배열을 만듭니다.
    for (int& x : a) std::cin >> x;  // 여기서는 참조 x로 읽어 실제 배열 원소를 수정해야 합니다.
    std::cout << total(a) << '\n';
    return 0;
}
// 함수 순회 O(N), 입력 저장 공간 O(N). vector 인자의 전달 방식에 따라 복사 비용이 달라진다.
