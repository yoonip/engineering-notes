#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

// picture는 값으로 전달되어 함수 안에서 지워도 호출자의 그림은 보존됨.
vector<int> solution(int m, int n, vector<vector<int>> picture) {
    int areas = 0, largest = 0;
    // 네 방향의 행 변화량.
    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    // ++는 1 증가.
    for (int row = 0; row < m; ++row) {
        for (int col = 0; col < n; ++col) {
            // 최대 색 값도 int 범위에 포함.
            int color = picture[row][col];
            if (color == 0) continue;
            ++areas;
            // 시작 칸 방문 표시.
            picture[row][col] = 0;
            vector<pair<int, int>> stack{{row, col}};
            // 현재 영역 넓이.
            int size = 0;
            while (!stack.empty()) {
                // back은 마지막 좌표 조회.
                auto point = stack.back();
                stack.pop_back();
                ++size;
                // 네 방향 이웃 검사.
                for (int direction = 0; direction < 4; ++direction) {
                    int nr = point.first + dr[direction];
                    // 다음 열 계산.
                    int nc = point.second + dc[direction];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && picture[nr][nc] == color) {
                        // 넣을 때 방문 표시해 같은 칸 중복 탐색 방지.
                        picture[nr][nc] = 0;
                        stack.push_back({nr, nc});
                    }
                }
            }
            // 현재 영역 넓이와 최대값 비교.
            largest = max(largest, size);
        }
    }
    return {areas, largest};
}
