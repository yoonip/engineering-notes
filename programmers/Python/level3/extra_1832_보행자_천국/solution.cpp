// vector는 가변 길이 배열.
#include <vector>
// std 이름 공간의 vector를 접두사 없이 사용.
using namespace std;

// {}는 함수 영역.
int solution(int m, int n, vector<vector<int>> city_map) {
    // 경로 수 나머지 기준.
    const int MOD = 20170805;
    // 열별 아래 방향 경로 수를 0으로 초기화.
    vector<int> vertical(n, 0);
    // 시작점에 가상 경로 하나 입력.
    vertical[0] = 1;
    // 왼쪽에서 오는 경로 수.
    int horizontal = 0;
    // ++는 1 증가.
    for (int row = 0; row < m; ++row) {
        // 새 행의 왼쪽 밖에서는 진입 불가능.
        horizontal = 0;
        // 왼쪽에서 오른쪽으로 열 순회.
        for (int col = 0; col < n; ++col) {
            if (city_map[row][col] == 1) {
                // 양 방향 경로 차단.
                vertical[col] = horizontal = 0;
            // 회전 가능한 일반 도로.
            } else if (city_map[row][col] == 0) {
                // 두 방향의 도착 경로 합계.
                int total = (vertical[col] + horizontal) % MOD;
                // 2칸에서는 두 방향 값을 그대로 유지.
                vertical[col] = horizontal = total;
            }
        }
    }
    // 목적지에서 합산된 경로 수 반환.
    return horizontal;
}
