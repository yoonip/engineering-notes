#include <array>
#include <iostream>
#include <queue>
#include <string>
#include <utility>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;
    if (!(std::cin >> n >> m) || n <= 0 || m <= 0) return 0;

    std::vector<std::string> grid(n);
    for (std::string &row : grid) std::cin >> row;

    std::vector<std::vector<int>> distance(n, std::vector<int>(m, 0));
    std::queue<std::pair<int, int>> queue;
    if (grid[0][0] == '1') {
        distance[0][0] = 1;
        queue.push({0, 0});
    }

    constexpr std::array<int, 4> dr{-1, 1, 0, 0};
    constexpr std::array<int, 4> dc{0, 0, -1, 1};

    while (!queue.empty()) {
        const auto [r, c] = queue.front();
        queue.pop();

        for (int direction = 0; direction < 4; ++direction) {
            int nr = r + dr[direction];
            int nc = c + dc[direction];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
            if (grid[nr][nc] != '1' || distance[nr][nc] != 0) continue;

            distance[nr][nc] = distance[r][c] + 1;
            queue.push({nr, nc});
        }
    }

    int answer = distance[n - 1][m - 1];
    std::cout << (answer == 0 ? -1 : answer) << '\n';
    return 0;
}
