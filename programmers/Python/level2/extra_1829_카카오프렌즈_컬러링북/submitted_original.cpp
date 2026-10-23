#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

vector<int> solution(int m, int n, vector<vector<int>> picture) {
    int areas = 0, largest = 0;
    int dr[4] = {1, -1, 0, 0};
    int dc[4] = {0, 0, 1, -1};
    for (int row = 0; row < m; ++row) {
        for (int col = 0; col < n; ++col) {
            int color = picture[row][col];
            if (color == 0) continue;
            ++areas;
            picture[row][col] = 0;
            vector<pair<int, int>> stack{{row, col}};
            int size = 0;
            while (!stack.empty()) {
                auto point = stack.back();
                stack.pop_back();
                ++size;
                for (int direction = 0; direction < 4; ++direction) {
                    int nr = point.first + dr[direction];
                    int nc = point.second + dc[direction];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && picture[nr][nc] == color) {
                        picture[nr][nc] = 0;
                        stack.push_back({nr, nc});
                    }
                }
            }
            largest = max(largest, size);
        }
    }
    return {areas, largest};
}

// 전체 코드 줄별 설명
// #include <vector>  // #include는 헤더 가져오기. vector는 가변 길이 배열.
// #include <utility>  // pair는 두 값을 묶는 좌표 자료형.
// #include <algorithm>  // max는 최댓값 계산.
// using namespace std;  // std 이름 공간 도구 사용.
// 
// vector<int> solution(int m, int n, vector<vector<int>> picture) {  // vector<int>는 정수 배열 반환형. picture는 값으로 전달되어 함수 안에서 지워도 호출자의 그림은 보존됨.
//     int areas = 0, largest = 0;  // int는 정수. 영역 수·최대 넓이 초기화.
//     int dr[4] = {1, -1, 0, 0};  // 고정 배열. 네 방향의 행 변화량.
//     int dc[4] = {0, 0, 1, -1};  // 네 방향의 열 변화량.
//     for (int row = 0; row < m; ++row) {  // 모든 행 순회. ++는 1 증가.
//         for (int col = 0; col < n; ++col) {  // 모든 열 순회.
//             int color = picture[row][col];  // []로 색 조회. 최대 색 값도 int 범위에 포함.
//             if (color == 0) continue;  // ==는 같음, continue는 이번 칸 건너뜀. 빈칸·방문 완료 칸 제외.
//             ++areas;  // 새 연결 영역 하나 추가.
//             picture[row][col] = 0;  // 시작 칸 방문 표시.
//             vector<pair<int, int>> stack{{row, col}};  // vector를 후입선출 스택으로 사용. pair에 행·열 저장, {}는 초기값.
//             int size = 0;  // 현재 영역 넓이.
//             while (!stack.empty()) {  // !는 부정, empty는 비었는지 검사. 탐색할 칸이 있는 동안 DFS.
//                 auto point = stack.back();  // auto는 타입 추론. back은 마지막 좌표 조회.
//                 stack.pop_back();  // pop_back은 마지막 원소 삭제.
//                 ++size;  // 방문한 칸 하나를 넓이에 추가.
//                 for (int direction = 0; direction < 4; ++direction) {  // 네 방향 이웃 검사.
//                     int nr = point.first + dr[direction];  // .first는 pair의 행. 다음 행 계산.
//                     int nc = point.second + dc[direction];  // .second는 열. 다음 열 계산.
//                     if (nr >= 0 && nr < m && nc >= 0 && nc < n && picture[nr][nc] == color) {  // &&는 모두 참. 범위 안·같은 색·미방문 조건 확인.
//                         picture[nr][nc] = 0;  // 넣을 때 방문 표시해 같은 칸 중복 탐색 방지.
//                         stack.push_back({nr, nc});  // push_back은 스택 끝에 좌표 추가.
//                     }  // 이웃 조건 종료.
//                 }  // 방향 순회 종료.
//             }  // 연결 영역 탐색 종료.
//             largest = max(largest, size);  // 현재 영역 넓이와 최대값 비교.
//         }  // 열 순회 종료.
//     }  // 행 순회 종료.
//     return {areas, largest};  // {}로 두 원소 정수 배열을 만들어 반환.
// }  // 함수 종료.

// 풀이 요약
// 0이 아닌 미방문 칸을 찾으면 새 영역을 시작하고 같은 색의 상하좌우 칸을 DFS로 전부 탐색한다. 영역별 넓이를 세어 최대값을 갱신한다.
// 방문한 칸은 복사한 그림에서 0으로 지워 재방문을 막는다. 대각선만 맞닿은 같은 색은 별개 영역이다.
// 예제는 영역 4개·최대 넓이 5. 모든 칸을 한 번씩 방문하므로 시간 O(MN), 그림 복사와 스택 공간 O(MN).
// 