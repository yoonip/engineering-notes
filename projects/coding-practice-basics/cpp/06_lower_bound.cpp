#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, q;
    if (!(std::cin >> n >> q) || n <= 0 || q <= 0) return 0;

    std::vector<long long> values(n);
    for (long long &value : values) std::cin >> value;

    while (q--) {
        long long target;
        std::cin >> target;

        auto it = std::lower_bound(values.begin(), values.end(), target);
        if (it != values.end() && *it == target) {
            std::cout << (it - values.begin()) << '\n';
        } else {
            std::cout << -1 << '\n';
        }
    }
    return 0;
}
