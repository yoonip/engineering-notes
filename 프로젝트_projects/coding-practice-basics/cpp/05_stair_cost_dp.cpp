#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n) || n <= 0) return 0;

    std::vector<long long> cost(n);
    for (long long &value : cost) std::cin >> value;

    std::vector<long long> best(n);
    best[0] = cost[0];
    if (n >= 2) best[1] = cost[0] + cost[1];

    for (int i = 2; i < n; ++i) {
        best[i] = std::min(best[i - 1], best[i - 2]) + cost[i];
    }

    std::cout << best[n - 1] << '\n';
    return 0;
}
