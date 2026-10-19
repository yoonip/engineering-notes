#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<double> voltage{3.1, 3.2, 3.3};
    const double sum = std::accumulate(voltage.begin(), voltage.end(), 0.0);
    std::cout << sum / voltage.size() << '\n';
}
