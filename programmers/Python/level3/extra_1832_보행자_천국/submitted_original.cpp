#include <vector>
using namespace std;

int solution(int m, int n, vector<vector<int>> city_map) {
    const int MOD = 20170805;
    vector<int> vertical(n, 0);
    vertical[0] = 1;
    int horizontal = 0;
    for (int row = 0; row < m; ++row) {
        horizontal = 0;
        for (int col = 0; col < n; ++col) {
            if (city_map[row][col] == 1) {
                vertical[col] = horizontal = 0;
            } else if (city_map[row][col] == 0) {
                int total = (vertical[col] + horizontal) % MOD;
                vertical[col] = horizontal = total;
            }
        }
    }
    return horizontal;
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 가져오기. vector는 가변 길이 배열.
// using namespace std;  // std 이름 공간의 vector를 접두사 없이 사용.
// 
// int solution(int m, int n, vector<vector<int>> city_map) {  // int는 정수, 중첩 vector는 도로 표. {}는 함수 영역.
//     const int MOD = 20170805;  // const는 변경 불가 상수. 경로 수 나머지 기준.
//     vector<int> vertical(n, 0);  // 열별 아래 방향 경로 수를 0으로 초기화.
//     vertical[0] = 1;  // 시작점에 가상 경로 하나 입력.
//     int horizontal = 0;  // 왼쪽에서 오는 경로 수.
//     for (int row = 0; row < m; ++row) {  // 행을 위에서 아래로 순회. ++는 1 증가.
//         horizontal = 0;  // 새 행의 왼쪽 밖에서는 진입 불가능.
//         for (int col = 0; col < n; ++col) {  // 왼쪽에서 오른쪽으로 열 순회.
//             if (city_map[row][col] == 1) {  // ==는 같음. 벽인 경우.
//                 vertical[col] = horizontal = 0;  // 양 방향 경로 차단.
//             } else if (city_map[row][col] == 0) {  // else if는 추가 조건. 회전 가능한 일반 도로.
//                 int total = (vertical[col] + horizontal) % MOD;  // %는 나머지. 두 방향의 도착 경로 합계.
//                 vertical[col] = horizontal = total;  // 아래·오른쪽으로 모두 나갈 수 있음. 2칸에서는 두 방향 값을 그대로 유지.
//             }  // 도로 종류 분기 종료.
//         }  // 열 반복 종료.
//     }  // 행 반복 종료.
//     return horizontal;  // 목적지에서 합산된 경로 수 반환.
// }  // 함수 종료.

// 풀이 요약
// vertical[c]는 위에서 내려온 경로 수, horizontal은 왼쪽에서 온 경로 수다. 자유 통행 칸에서는 두 수를 합쳐 어느 방향으로도 출발할 수 있다.
// 벽에서는 두 수를 0으로 만들고, 직진 전용 칸에서는 두 수를 섞지 않고 그대로 전달한다. 예제 2는 방향 전환을 제한하면 두 경로만 남는다.
// 시작점 위에서 경로 하나가 들어온 것으로 초기화한다. 시간 O(MN), 추가 공간 O(N).
// 