#include <vector>
#include <algorithm>
#include <cstdlib>
#include <utility>
using namespace std;

int solution(int n, int m, vector<vector<int>> timetable) {
    vector<int> delta(1322, 0);
    for (auto interval : timetable) {
        ++delta[interval[0]];
        --delta[interval[1] + 1];
    }
    int current = 0, peak = 0;
    for (int change : delta) {
        current += change;
        peak = max(peak, current);
    }
    if (peak <= 1) return 0;
    for (int distance = 2 * n - 2; distance >= 1; --distance) {
        for (int offset = 0; offset < n; ++offset) {
            vector<pair<int, int>> placed;
            for (int position = offset; position < n * n; ++position) {
                int row = position / n, col = position % n;
                bool valid = true;
                for (auto point : placed) {
                    if (abs(row - point.first) + abs(col - point.second) < distance) {
                        valid = false;
                        break;
                    }
                }
                if (valid) {
                    placed.push_back({row, col});
                    if (placed.size() == peak) return distance;
                }
            }
        }
    }
    return 1;
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 가져오기. vector는 크기를 바꿀 수 있는 배열.
// #include <algorithm>  // algorithm은 max 등 알고리즘 함수 제공.
// #include <cstdlib>  // cstdlib은 정수 abs(절댓값) 제공.
// #include <utility>  // utility는 두 값을 묶는 pair 제공.
// using namespace std;  // std 이름 공간의 도구를 접두사 없이 사용. ;는 문장 끝.
// 
// int solution(int n, int m, vector<vector<int>> timetable) {  // int는 정수, 함수 정의. 중첩 vector는 예약 시각 표, {}는 함수 영역.
//     vector<int> delta(1322, 0);  // 1322개 정수를 0으로 초기화한 변화량 배열.
//     for (auto interval : timetable) {  // auto는 타입 추론. 범위 for로 예약 하나씩 복사.
//         ++delta[interval[0]];  // ++는 1 증가, []는 인덱스 조회. 입실 인원 추가.
//         --delta[interval[1] + 1];  // --는 1 감소. 퇴실 시각 다음 분에 제외.
//     }  // 예약 반복 종료.
//     int current = 0, peak = 0;  // 현재·최대 동시 인원 초기화.
//     for (int change : delta) {  // 변화량을 시간순으로 순회.
//         current += change;  // +=는 더해 저장.
//         peak = max(peak, current);  // 최대 동시 인원 갱신.
//     }  // 시간 순회 종료.
//     if (peak <= 1) return 0;  // if는 조건 분기, return은 반환. 겹치는 손님이 없으면 0.
//     for (int distance = 2 * n - 2; distance >= 1; --distance) {  // 가능한 최대 맨해튼 거리부터 감소시키며 검사.
//         for (int offset = 0; offset < n; ++offset) {  // 첫 행의 시작 열을 모두 시도.
//             vector<pair<int, int>> placed;  // pair는 행·열 묶음. 선택한 락커 목록.
//             for (int position = offset; position < n * n; ++position) {  // 행 우선으로 모든 뒤쪽 칸 검사.
//                 int row = position / n, col = position % n;  // 정수 /는 몫, %는 나머지. 행·열 복원.
//                 bool valid = true;  // bool은 참·거짓 자료형. 배치 가능 여부 초기화.
//                 for (auto point : placed) {  // 이미 선택한 모든 락커와 비교.
//                     if (abs(row - point.first) + abs(col - point.second) < distance) {  // .first·.second는 pair의 두 값. 맨해튼 거리가 부족하면 실패.
//                         valid = false;  // 거짓으로 표시.
//                         break;  // 가장 가까운 for 반복 종료.
//                     }  // 거리 조건 분기 종료.
//                 }  // 기존 배치 비교 종료.
//                 if (valid) {  // 모든 기존 락커와 충분히 떨어져 있으면 배치.
//                     placed.push_back({row, col});  // push_back은 배열 끝에 추가. {}로 좌표 pair 생성.
//                     if (placed.size() == peak) return distance;  // size는 원소 수, ==는 같음. 필요 인원 배치 성공 시 거리 반환.
//                 }  // 배치 분기 종료.
//             }  // 칸 순회 종료.
//         }  // 시작 열 순회 종료.
//     }  // 거리 후보 순회 종료.
//     return 1;  // 최소 간격 1 반환.
// }  // 정답 함수 종료.

// 풀이 요약
// 예약 구간의 양 끝을 포함해 최대 동시 인원 K를 센다. K개의 충분히 떨어진 락커를 준비하면 예약은 빈 락커로 배정할 수 있다.
// 거리를 큰 값부터 내리며 첫 행의 시작 열을 바꾼 행 우선 배치를 검사한다. 첫 모서리만 쓰면 n=4,K=3의 거리 4 배치를 놓칠 수 있다.
// 거리 후보 O(N), 시작 열 O(N), 칸 O(N²), 거리 비교 O(N²)로 상한 O(N⁶). N≤10이며 인원을 채우면 즉시 종료한다.
// 