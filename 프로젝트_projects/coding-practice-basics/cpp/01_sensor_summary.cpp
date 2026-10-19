#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n) || n <= 0) return 0;

    std::vector<long long> values(n);
    long long sum = 0;
    for (long long &value : values) {
        std::cin >> value;
        sum += value;
    }

    const auto [minimum, maximum] = std::minmax_element(values.begin(), values.end());
    std::cout << *minimum << ' ' << *maximum << ' ' << sum << '\n';
    return 0;
}
