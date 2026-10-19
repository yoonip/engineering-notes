#include <array>
#include <iostream>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string digits;
    if (!(std::cin >> digits)) return 0;

    std::array<int, 10> frequency{};
    for (char ch : digits) {
        if (ch >= '0' && ch <= '9') ++frequency[ch - '0'];
    }

    for (int digit = 0; digit < 10; ++digit) {
        if (digit > 0) std::cout << ' ';
        std::cout << frequency[digit];
    }
    std::cout << '\n';
    return 0;
}
