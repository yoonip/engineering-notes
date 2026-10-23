// vector는 크기를 바꿀 수 있는 배열.
#include <vector>
// algorithm은 max 등 알고리즘 함수 제공.
#include <algorithm>
// cstdlib은 정수 abs(절댓값) 제공.
#include <cstdlib>
// utility는 두 값을 묶는 pair 제공.
#include <utility>
using namespace std;

// 중첩 vector는 예약 시각 표, {}는 함수 영역.
int solution(int n, int m, vector<vector<int>> timetable) {
    // 1322개 정수를 0으로 초기화한 변화량 배열.
    vector<int> delta(1322, 0);
    // 범위 for로 예약 하나씩 복사.
    for (auto interval : timetable) {
        // 입실 인원 추가.
        ++delta[interval[0]];
        // 퇴실 시각 다음 분에 제외.
        --delta[interval[1] + 1];
    }
    // 현재·최대 동시 인원 초기화.
    int current = 0, peak = 0;
    // 변화량을 시간순으로 순회.
    for (int change : delta) {
        // +=는 더해 저장.
        current += change;
        // 최대 동시 인원 갱신.
        peak = max(peak, current);
    }
    // 겹치는 손님이 없으면 0.
    if (peak <= 1) return 0;
    // 가능한 최대 맨해튼 거리부터 감소시키며 검사.
    for (int distance = 2 * n - 2; distance >= 1; --distance) {
        // 첫 행의 시작 열을 모두 시도.
        for (int offset = 0; offset < n; ++offset) {
            // 선택한 락커 목록.
            vector<pair<int, int>> placed;
            // 행 우선으로 모든 뒤쪽 칸 검사.
            for (int position = offset; position < n * n; ++position) {
                int row = position / n, col = position % n;
                // 배치 가능 여부 초기화.
                bool valid = true;
                // 이미 선택한 모든 락커와 비교.
                for (auto point : placed) {
                    // 맨해튼 거리가 부족하면 실패.
                    if (abs(row - point.first) + abs(col - point.second) < distance) {
                        valid = false;
                        // 가장 가까운 for 반복 종료.
                        break;
                    }
                }
                // 모든 기존 락커와 충분히 떨어져 있으면 배치.
                if (valid) {
                    // {}로 좌표 pair 생성.
                    placed.push_back({row, col});
                    // 필요 인원 배치 성공 시 거리 반환.
                    if (placed.size() == peak) return distance;
                }
            }
        }
    }
    // 최소 간격 1 반환.
    return 1;
}
